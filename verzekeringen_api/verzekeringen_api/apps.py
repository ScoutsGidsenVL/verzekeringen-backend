import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)


class InsuranceConfig(AppConfig):
    name = "insurance"

    def ready(self):
        from . import signal_receiver

        logger.debug("insurance")
