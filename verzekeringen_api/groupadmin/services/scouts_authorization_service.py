import logging
from typing import List

from django.conf import settings

from scouts_auth.services import AuthorizationService

from groupadmin.models import ScoutsGroup
from groupadmin.services import GroupAdmin
from groupadmin.utils import SettingsHelper


logger = logging.getLogger(__name__)


class ScoutsAuthorizationService(AuthorizationService):

    USER = "role_user"
    SECTION_LEADER = "role_section_leader"
    GROUP_LEADER = "role_group_leader"
    DISTRICT_COMMISSIONER = "role_district_commissioner"
    ADMINISTRATOR = "role_administrator"

    known_roles = [USER, SECTION_LEADER, GROUP_LEADER, DISTRICT_COMMISSIONER, ADMINISTRATOR]

    def load_user_scouts_groups(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        service = GroupAdmin()

        scouts_groups: List[ScoutsGroup] = service.get_groups(active_user=user).groups

        user.scouts_groups = scouts_groups

        user = self.update_user_scouts_groups(user)

        logger.debug("USER PERMISSIONS: %s", user.user_permissions)

    def update_user_scouts_groups(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        """
        Updates the authenticated user with the groups he/she belongs to.

        The groupadmin call for groups can only be made after the user has been authenticated.
        """
        user: settings.AUTH_USER_MODEL = self.update_user_authorizations(user)

        user.full_clean()
        user.save()

        permissions = user.get_all_permissions()
        logger.debug("PERMISSIONS: %s", permissions)
        logger.debug("GROUPS: %s", user.groups.all())
        logger.debug("ADMINISTRATOR ?: %s", user.is_administrator)
        logger.debug("DISTRICT_COMMISSIONER ?: %s", user.is_district_commissioner)

        return user

    def update_user_authorizations(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        # Initialize authorizations we can derive from membership of a scouts group
        if user.has_role_administrator():
            user = self.add_user_as_admin(user)

        if user.has_role_district_commissioner():
            user = self.add_user_to_group(user, ScoutsAuthorizationService.DISTRICT_COMMISSIONER)

        if SettingsHelper.is_debug():
            test_groups = SettingsHelper.get_test_groups()
            if any(group in user.get_group_names() for group in test_groups):
                logger.debug(
                    "User %s is member of a test group and DEBUG is set to True, adding user as administrator",
                    user.username,
                )
                user = self.add_user_as_admin(user)

        return user

    def add_user_as_admin(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        return self.add_user_to_group(user, ScoutsAuthorizationService.ADMINISTRATOR)

    def add_user_to_group(self, user: settings.AUTH_USER_MODEL, role: str) -> settings.AUTH_USER_MODEL:
        if role not in self.known_roles:
            raise ValueError("Role " + role + " is not a known scouts role")

        super().add_user_to_group(user, group_name=role)

        return user
