import logging

from rest_framework import serializers

from scouts_auth.models import GroupAdminMemberSearchResponse, GroupAdminMemberSearchMember
from scouts_auth.serializers import GroupAdminResponseSerializer, GroupAdminLinkSerializer


logger = logging.getLogger(__name__)


class GroupAdminMemberSearchMemberSerializer(serializers.Serializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "group_admin_id": data.pop("id", ""),
            "first_name": data.pop("voornaam", ""),
            "last_name": data.pop("achternaam", ""),
            "birth_date": data.pop("", None),
            "email": data.pop("email", ""),
            "phone": data.pop("gsm", ""),
            "links": GroupAdminLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GroupAdminMemberSearchMember:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminMemberSearchMember:
        instance = GroupAdminMemberSearchMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", "")
        instance.first_name = validated_data.pop("first_name", "")
        instance.last_name = validated_data.pop("last_name", "")
        instance.birth_date = validated_data.pop("birth_date", None)
        instance.email = validated_data.pop("email", "")
        instance.phone = validated_data.pop("phone", "")
        instance.links = GroupAdminLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class GroupAdminMemberSearchResponseSerializer(GroupAdminResponseSerializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "members": GroupAdminMemberSearchMemberSerializer(many=True).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GroupAdminMemberSearchResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminMemberSearchResponse:
        instance = GroupAdminMemberSearchResponse()

        super().create(validated_data)

        instance.members = GroupAdminMemberSearchMemberSerializer(many=True).create(validated_data.pop("members", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
