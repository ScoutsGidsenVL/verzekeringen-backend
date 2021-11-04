import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import GroupAdminLink

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class GroupAdminLinkSerializer(NonModelSerializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "rel": data.pop("rel", ""),
            "href": data.pop("href", ""),
            "method": data.pop("method", ""),
            "sections": data.pop("secties", []),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GroupAdminLink:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminLink:
        instance = GroupAdminLink()

        instance.rel = validated_data.pop("rel", "")
        instance.href = validated_data.pop("href", "")
        instance.method = validated_data.pop("method", "")
        instance.sections = validated_data.pop("sections", [])

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
