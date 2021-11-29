import logging

from scouts_auth.inuits.utils import Singleton


logger = logging.getLogger(__name__)


@Singleton
class GlobalSettingsUtil:

    _is_test = False

    def __init__(self):
        logger.debug("CREATED GlobalSettingsUtil")

    @property
    def is_test(self) -> bool:
        return self._is_test

    @is_test.setter
    def is_test(self, is_test: bool):
        logger.debug("SETTING is_test to %s", is_test)
        self._is_test = is_test
