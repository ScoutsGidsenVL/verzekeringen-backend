"""apps.signals.apps."""

import logging

from django.apps import AppConfig

logger = logging.getLogger(__name__)


class InsuranceSignalsConfig(AppConfig):
    name = "apps.signals"

    def ready(self):
        import scouts_auth.auth.signals

        from .signal_handler import InsuranceSignalHandler

        logger.debug("insurance app is ready")
