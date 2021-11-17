import logging
from typing import List

from django.conf import settings
from django.dispatch import receiver

from scouts_auth.signals import ScoutsAuthSignalSender, app_ready, authenticated
from scouts_auth.services import PermissionService

from groupadmin.models import ScoutsGroup
from groupadmin.services import GroupAdmin, ScoutsOIDCAuthenticationBackend


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
        Reads additional data for a user and takes appropriate action

        Some user data necessary for permissions can only be loaded by a profile call, after authentication,
        this method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        logger.debug("SIGNAL received: 'authenticated' from %s", ScoutsAuthSignalSender.sender)

        service = GroupAdmin()

        scouts_groups: List[ScoutsGroup] = service.get_groups(active_user=user).groups

        user.scouts_groups = scouts_groups

        ScoutsOIDCAuthenticationBackend().update_user_scouts_groups(user)

        logger.debug("USER PERMISSIONS: %s", user.user_permissions)

        return user
