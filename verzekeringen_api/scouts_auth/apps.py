import logging


from django.apps import AppConfig


logger = logging.getLogger(__name__)


class ScoutsAuthConfig(AppConfig):
    name = "scouts_auth"

    def ready(self):
        logger.debug("SCOUTS-AUTH: app is ready")
