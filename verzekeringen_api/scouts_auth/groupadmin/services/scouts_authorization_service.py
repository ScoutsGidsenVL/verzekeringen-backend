import logging
from typing import List
from datetime import datetime

from django.conf import settings

from scouts_auth.auth.services import AuthorizationService

from scouts_auth.groupadmin.models import AbstractScoutsFunction
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.groupadmin.utils import SettingsHelper

from scouts_auth.inuits.utils import GlobalSettingsUtil, DateUtils


logger = logging.getLogger(__name__)


class ScoutsAuthorizationService(AuthorizationService):
    """
    Fetches additional information from groupadmin, required to finetune user permissions.

    For a scouts user, the following sources are required for full authorization:
    0) Successfull authentication (provides partial scouts groups)
    1) Full user information, after a groupadmin call to /profiel (the "me" call)
    2) BASIC PERMISSIONS: Membership of groups, defined in roles.yaml and loaded by PermissionService
    3) ADMINISTRATOR: Membership of administrator groups, from the user informatiom (/profiel)
    4) SECTION LEADER: every user that is not an administrator

    The roles role_group_leader and role_district_commissioner were removed (T7607): they were never assigned
    or only granted permissions the user already had through the section leader role.
    """

    SECTION_LEADER = "role_section_leader"
    ADMINISTRATOR = "role_administrator"

    known_roles = [SECTION_LEADER, ADMINISTRATOR]

    service = GroupAdminMemberService()

    def update_user_authorizations(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        # Initialize authorizations we can derive from membership of a scouts group
        if user.has_role_administrator():
            user = self.add_user_as_admin(user)
        else:
            user = self.add_user_to_group(user, ScoutsAuthorizationService.SECTION_LEADER)

        # if user.has_role_section_leader():
        #     user = self.add_user_to_group(user, ScoutsAuthorizationService.SECTION_LEADER)

        if SettingsHelper.is_debug():
            test_groups = SettingsHelper.get_test_groups()
            if any(group in user.get_group_names() for group in test_groups):
                logger.debug(
                    "User %s is member of a test group and DEBUG is set to True, adding user as administrator",
                    user.username,
                )
                GlobalSettingsUtil.instance().is_test = True
                user = self.add_user_as_admin(user)

        return user

    def add_user_as_admin(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        return self.add_user_to_group(user, ScoutsAuthorizationService.ADMINISTRATOR)

    def add_user_to_group(self, user: settings.AUTH_USER_MODEL, role: str) -> settings.AUTH_USER_MODEL:
        if role not in self.known_roles:
            raise ValueError("Role " + role + " is not a known scouts role")

        super().add_user_to_group(user, group_name=role)

        return user

    def load_user_functions(self, user: settings.AUTH_USER_MODEL) -> settings.AUTH_USER_MODEL:
        functions: List[AbstractScoutsFunction] = self.service.get_functions(active_user=user).functions
        for user_function in user.functions:
            for function in functions:
                if (
                    function.group_admin_id == user_function.group_admin_id
                    or function.group_admin_id == user_function.function
                ):
                    for grouping in function.groupings:
                        if grouping.name == SettingsHelper.get_section_leader_identifier():
                            logger.debug(
                                "Setting user as section leader for group %s",
                                user_function.scouts_group.group_admin_id,
                            )
                            user_function.groups_section_leader[user_function.scouts_group.group_admin_id] = True

        user.full_clean()
        user.save()

        return user
