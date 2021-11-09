import logging

from django.dispatch import receiver

from scouts_auth.signals import app_ready, authenticated


logger = logging.getLogger(__name__)


class ScoutsAuthSignalCatcher:
    @receiver(app_ready)
    def handle_app_ready(sender, **kwargs):
        logger.debug("INSURANCE: app_ready")

    @receiver(authenticated)
    def handle_authenticated(sender, **kwargs):
        logger.debug("INSURANCE: Authenticated")
