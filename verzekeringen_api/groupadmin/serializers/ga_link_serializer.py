import logging
from typing import List

from rest_framework import serializers

from groupadmin.models import ScoutsLink

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsLinkSectionSerializer(NonModelSerializer):
    def to_internal_value(self, data: List[str]) -> list:
        if data is None:
            return None

        logger.debug("SECTIONS: %s", data)

        return data

    def save(self) -> List[str]:
        return self.create(self.validated_data)

    def create(self, validated_data: List[str]) -> List[str]:
        if validated_data is None:
            return None

        logger.debug("SECTIONS: %s", validated_data)

        return validated_data


class ScoutsLinkSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "rel": data.pop("rel", None),
            "href": data.pop("href", None),
            "method": data.pop("method", None),
            "sections": ScoutsLinkSectionSerializer().to_internal_value(data.pop("secties", None)),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsLink:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsLink:
        if validated_data is None:
            return None

        instance = ScoutsLink()

        instance.rel = validated_data.pop("rel", None)
        instance.href = validated_data.pop("href", None)
        instance.method = validated_data.pop("method", None)
        instance.sections = ScoutsLinkSectionSerializer().create(validated_data.pop("sections", None))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
