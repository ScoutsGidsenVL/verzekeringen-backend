import logging

from rest_framework import serializers

from scouts_auth.models import GroupAdminResponse
from scouts_auth.serializers import GroupAdminLinkSerializer


logger = logging.getLogger(__name__)


class GroupAdminResponseSerializer(serializers.Serializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "count": data.pop("aantal", ""),
            "total": data.pop("totaal", ""),
            "offset": data.pop("offset", ""),
            "filter_criterium": data.pop("filtercriterium", ""),
            "criteria": data.pop("criteria", {}),
            "links": GroupAdminLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GroupAdminResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminResponse:
        instance = GroupAdminResponse()

        instance.count = validated_data.pop("count", 0)
        instance.total = validated_data.pop("total", 0)
        instance.offset = validated_data.pop("offset", 0)
        instance.filter_criterium = validated_data.pop("filter_criterium", "")
        instance.criteria = validated_data.pop("criteria", {})
        instance.links = GroupAdminLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
