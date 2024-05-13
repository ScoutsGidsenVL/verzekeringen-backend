import logging

from django.conf import settings

logger = logging.getLogger(__name__)


class SettingsHelper:
    @staticmethod
    def get_attribute(attribute_name: str, attribute_default_value: any = None, log_missing: str = None) -> any:
        if log_missing is None:
            return getattr(settings, attribute_name, attribute_default_value)

        setting = getattr(settings, attribute_name)
        if setting is None:
            logger.debug("NO SUCH SETTING: %s", attribute_name)
            return attribute_default_value

        return setting

    @staticmethod
    def get(attribute_name: str, attribute_default_value: str = None, log_missing: str = None) -> str:
        return str(SettingsHelper.get_attribute(attribute_name, attribute_default_value, log_missing))

    @staticmethod
    def get_bool(attribute_name: str, attribute_default_value: bool = False, log_missing: str = None) -> bool:
        return bool(SettingsHelper.get_attribute(attribute_name, attribute_default_value, log_missing))
