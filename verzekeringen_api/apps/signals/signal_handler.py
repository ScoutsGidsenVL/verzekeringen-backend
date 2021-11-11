import logging

from django.dispatch import receiver

from scouts_auth.signals import ScoutsAuthSignalSender, app_ready, authenticated
from scouts_auth.models import User
from scouts_auth.services import PermissionService


logger = logging.getLogger(__name__)


class InsuranceSignalHandler:
    @staticmethod
    @receiver(app_ready, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.app_ready_uid)
    def handle_app_ready(**kwargs):
        logger.debug("SIGNAL received: 'app_ready' from %s", ScoutsAuthSignalSender.sender)

        PermissionService().populate_roles()

    @staticmethod
    @receiver(
        authenticated, sender=ScoutsAuthSignalSender.sender, dispatch_uid=ScoutsAuthSignalSender.authenticated_uid
    )
    def handle_authenticated(user: User, **kwargs):
        logger.debug("SIGNAL received: 'authenticated' from %s", ScoutsAuthSignalSender.sender)
