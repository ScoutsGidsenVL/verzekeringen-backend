import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import GroupAdminContact, GroupAdminLink
from scouts_auth.serializers import GroupAdminLinkSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class GroupAdminContactSerializer(NonModelSerializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "member": data.pop("oidLid", data.pop("lid", "")),
            "function": data.pop("oidFunctie", data.pop("functie", "")),
            "name": data.pop("naam", ""),
            "phone": data.pop("tel", ""),
            "email": data.pop("email", ""),
            "links": GroupAdminLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GroupAdminContact:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminContact:
        instance = GroupAdminContact()

        instance.member = validated_data.pop("member", "")
        instance.function = validated_data.pop("function", "")
        instance.name = validated_data.pop("name", "")
        instance.phone = validated_data.pop("phone", "")
        instance.email = validated_data.pop("email", "")
        instance.links = GroupAdminLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
