import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import MemberListMember, MemberList, GroupAdminLink
from . import GroupAdminLinkSerializer

from inuits.serializers import OptionalIntegerField


logger = logging.getLogger(__name__)


class MemberListMemberSerializer(serializers.Serializer):

    group_admin_id: str = serializers.CharField(source="id", default="")
    index: int = serializers.IntegerField(source="positie", default=0)
    values: dict = serializers.DictField(source="waarden", default={})
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, default=[])

    # class Meta:
    #     model = MemberListMember
    #     fields = "__all__"

    def save(self) -> MemberListMember:
        return self.create(self.validated_data)

    def create(self, **validated_data) -> MemberListMember:
        instance = MemberListMember()

        links_serializer = GroupAdminLinkSerializer(data=validated_data.pop("links", []), many=True)
        links_serializer.is_valid()
        links = links_serializer.save()

        instance.group_admin_id = validated_data.pop("id", "")
        instance.index = validated_data.pop("positie", 0)
        instance.values = validated_data.pop("waarden", {})
        instance.links = links

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class MemberListSerializer(serializers.Serializer):

    count: int = serializers.IntegerField(source="aantal", default=0)
    total: int = serializers.IntegerField(source="totaal", default=0)
    offset: int = serializers.IntegerField(default=0)
    filter_criterium: str = serializers.CharField(source="filtercriterium", default="")
    members: List[MemberListMember] = MemberListMemberSerializer(source="leden", many=True, default=[])
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, default=[])

    # class Meta:
    #     model = MemberList
    #     fields = "__all__"

    def save(self) -> MemberList:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data) -> MemberList:
        instance = MemberList()

        members_serializer = MemberListMemberSerializer(data=validated_data.pop("leden", []), many=True)
        members_serializer.is_valid(raise_exception=True)
        members = members_serializer.save()

        links_serializer = GroupAdminLinkSerializer(data=validated_data.pop("links", []), many=True)
        links_serializer.is_valid()
        links = links_serializer.save()

        instance.count = validated_data.pop("aantal", 0)
        instance.total = validated_data.pop("totaal", 0)
        instance.offset = validated_data.pop("offset", 0)
        instance.filter_criterium = validated_data.pop("filtercriterium", "")
        instance.members = members
        instance.links = links

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
