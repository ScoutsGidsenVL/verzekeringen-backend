import logging

from django.dispatch import Signal


logger = logging.getLogger(__name__)


app_ready = Signal()
authenticated = Signal()
