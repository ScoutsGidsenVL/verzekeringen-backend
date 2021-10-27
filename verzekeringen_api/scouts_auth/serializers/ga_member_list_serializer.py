import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import MemberListMember, MemberList, GroupAdminLink
from . import GroupAdminLinkSerializer


logger = logging.getLogger(__name__)


class MemberListMemberSerializer(serializers.Serializer):

    id: str = serializers.CharField(default="")
    values: dict = serializers.DictField(source="waarden", default=None)
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, required=False)

    class Meta:
        model = MemberListMember
        fields = "__all__"


class MemberListSerializer(serializers.Serializer):

    count: int = serializers.IntegerField(source="aantal", default=0)
    total: int = serializers.IntegerField(source="totaal", default=0)
    offset: int = serializers.IntegerField(default=0)
    members: List[MemberList] = MemberListMemberSerializer(source="leden", many=True)
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True)

    class Meta:
        model = MemberListMember
        fields = "__all__"
