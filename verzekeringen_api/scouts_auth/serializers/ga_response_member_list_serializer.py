import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import (
    GroupAdminMemberListMemberValue,
    GroupAdminMemberListMember,
    GroupAdminMemberListResponse,
)
from scouts_auth.serializers import GroupAdminLinkSerializer, GroupAdminResponseSerializer


logger = logging.getLogger(__name__)


class GroupAdminMemberListMemberValueSerializer(serializers.Serializer):
    def to_internal_value(self, data: tuple) -> dict:
        (key, value) = data
        validated_data = {"key": key, "value": value}

        return validated_data

    def save(self) -> GroupAdminMemberListMemberValue:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GroupAdminMemberListMemberValue:
        instance = GroupAdminMemberListMemberValue()

        instance.key = validated_data.pop("key", "")
        instance.value = validated_data.pop("value", "")

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GroupAdminMemberListMemberSerializer(serializers.Serializer):
    def to_internal_value(self, data: dict) -> dict:
        validated_data = {
            "group_admin_id": data.pop("id", ""),
            "index": data.pop("positie", 0),
            "values": GroupAdminMemberListMemberValueSerializer(many=True).to_internal_value(
                list(data.pop("waarden", {}).items())
            ),
            "links": GroupAdminLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> GroupAdminMemberListMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GroupAdminMemberListMember:
        instance = GroupAdminMemberListMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", "")
        instance.index = validated_data.pop("index", 0)
        instance.values = GroupAdminMemberListMemberValueSerializer(many=True).create(validated_data.pop("values", {}))
        instance.links = GroupAdminLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GroupAdminMemberListResponseSerializer(GroupAdminResponseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        validated_data = {
            "members": GroupAdminMemberListMemberSerializer(many=True).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> GroupAdminMemberListResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> GroupAdminMemberListResponse:
        instance = GroupAdminMemberListResponse()

        instance.members = GroupAdminMemberListMemberSerializer(many=True).create(validated_data.pop("members", []))

        super().create(validated_data)

        logger.debug("INSTANCE: %s", instance)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
