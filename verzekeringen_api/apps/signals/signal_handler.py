import logging
from typing import List

from django.conf import settings
from django.dispatch import receiver

from scouts_auth.signals import ScoutsAuthSignalSender, app_ready, authenticated
from scouts_auth.services import PermissionService

from groupadmin.services import ScoutsAuthorizationService


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

        Some user data necessary for permissions can only be loaded by a groupadmin profile call after authentication.
        This method handles a signal for the basic oidc authentication, then makes the necessary additional calls.
        """
        logger.debug("SIGNAL received: 'authenticated' from %s", ScoutsAuthSignalSender.sender)
        
        service = ScoutsAuthorizationService()

        logger.debug("SIGNAL handling for 'authenticated' -> Loading additional user groups")
        service.load_user_scouts_groups(user)
        logger.debug("SIGNAL handling for 'authenticated' -> Loading scouts functions")
        service.load_user_functions(user)

        return user
