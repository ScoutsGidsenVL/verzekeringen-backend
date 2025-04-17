import logging
from typing import List
from operator import attrgetter

from django.conf import settings
from django.dispatch import receiver

from scouts_auth.auth.services import PermissionService
from scouts_auth.auth.signals import ScoutsAuthSignalSender, app_ready, authenticated, refreshed

from scouts_auth.groupadmin.models import AbstractScoutsFunction, AbstractScoutsGroup
from scouts_auth.groupadmin.services import ScoutsAuthorizationService, GroupAdminMemberService
from scouts_auth.groupadmin.utils import SettingsHelper

logger = logging.getLogger(__name__)


class InsuranceSignalHandler:
    @staticmethod
    @receiver(app_ready, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.app_ready_uid)
    def handle_app_ready(**kwargs):
        logger.debug("SIGNAL received: 'app_ready' from %s", ScoutsAuthSignalSender.sender)
        try:
            PermissionService().populate_roles()
        except Exception as exc:
            logger.error("Unable to populate user roles", exc)

    @staticmethod
    @receiver(
        authenticated, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.authenticated_uid
    )
    def handle_authenticated(user: settings.AUTH_USER_MODEL, **kwargs) -> settings.AUTH_USER_MODEL:
        """
        Reads additional data for a user and takes appropriate action.

        Some user data necessary for permissions can only be loaded by a groupadmin profile call after authentication.
        This method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        logger.debug("SIGNAL received: 'authenticated' from %s", ScoutsAuthSignalSender.sender)

        groupadmin = GroupAdminMemberService()

        scouts_groups: List[AbstractScoutsGroup] = groupadmin.get_groups(active_user=user).scouts_groups
        user_scouts_groups: List[AbstractScoutsGroup] = []

        for scouts_group in scouts_groups:
            if (
                scouts_group.group_admin_id in SettingsHelper.get_administrator_groups()
                or scouts_group.is_leader
            ):
                if scouts_group.group_admin_id not in [g.group_admin_id for g in user_scouts_groups]:
                    user_scouts_groups.append(scouts_group)

        user_scouts_groups.sort(key=attrgetter('group_admin_id'))
        user.scouts_groups = user_scouts_groups
        logger.debug(user.to_descriptive_string())

        return user

    @staticmethod
    @receiver(refreshed, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.refreshed_uid)
    def handle_refreshed(user: settings.AUTH_USER_MODEL, **kwargs) -> settings.AUTH_USER_MODEL:
        logger.debug("SIGNAL received: 'refreshed' from %s", ScoutsAuthSignalSender.sender)
        # user.last_refreshed = timezone.now()
        # user.full_clean()
        # user.save()

        return user
