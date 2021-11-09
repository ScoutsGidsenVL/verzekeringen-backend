import logging


from django.apps import AppConfig

from scouts_auth.signals import ScoutsAuthSignalHandler


logger = logging.getLogger(__name__)


class ScoutsAuthConfig(AppConfig):
    name = "scouts_auth"

    handler = ScoutsAuthSignalHandler()

    def ready(self):
        self.handler.app_ready()
