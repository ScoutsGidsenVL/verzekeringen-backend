from typing import List

from rest_framework import serializers

from scouts_auth.models import GroupAdminContact, GroupAdminLink
from scouts_auth.serializers import GroupAdminLinkSerializer

from inuits.logging import InuitsLogger


logger = InuitsLogger(__name__)


class GroupAdminContactSerializer(serializers.Serializer):

    # member: str = serializers.CharField(source="lid", default="")
    # oid_member: str = serializers.CharField(source="oidLid", default="")
    # function: str = serializers.CharField(source="functie", default="")
    # oid_function: str = serializers.CharField(source="oidFunctie", default="")
    # name: str = serializers.CharField(source="naam", default="")
    # phone: str = serializers.CharField(source="tel", default="")
    # email: str = serializers.CharField(required=False, default="")
    # links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, default=[])

    class Meta:
        model = GroupAdminContact
        fields = "__all__"

    def save(self) -> GroupAdminContact:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminContact:
        instance = GroupAdminContact()

        links_serializer = GroupAdminLinkSerializer(data=validated_data.pop("links", []), many=True)
        links_serializer.is_valid(raise_exception=True)
        links: List[GroupAdminLink] = links_serializer.save()

        instance.member = validated_data.pop("lid", validated_data.pop("oidLid", ""))
        instance.function = validated_data.pop("functie", validated_data.pop("oidFunctie", ""))
        instance.name = validated_data.pop("naam", "")
        instance.phone = validated_data.pop("tel", "")
        instance.email = validated_data.pop("email", "")
        instance.links = links

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
