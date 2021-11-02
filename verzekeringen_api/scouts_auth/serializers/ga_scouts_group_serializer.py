import logging
from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import GroupAdminContact, ScoutsGroup, GroupAdminLink, GroupAdminAddress
from scouts_auth.serializers import GroupAdminLinkSerializer, GroupAdminAddressSerializer, GroupAdminContactSerializer


logger = logging.getLogger(__name__)


class ScoutsGroupSerializer(serializers.ModelSerializer):
    """Serializes a Group instance to a string."""

    # group_admin_id: str = serializers.CharField(default="")
    # number: str = serializers.CharField(source="groepsnummer", default="")
    # name: str = serializers.CharField(source="naam", default="")
    # addresses: List[GroupAdminAddress] = GroupAdminAddressSerializer(source="adressen", many=True, default=[])
    # date_of_foundation: date = serializers.DateTimeField(source="opgericht", default=None)
    # only_leaders: bool = serializers.BooleanField(source="enkelLeiding", default=False)
    # show_members_improved: bool = serializers.BooleanField(source="ledenVerbeterdTonen", default=False)
    # bank_account: str = serializers.CharField(source="rekeningnummer", default="")
    # email: str = serializers.CharField(default="")
    # website: str = serializers.CharField(default="")
    # info: str = serializers.CharField(source="vrijeInfo", default="")
    # type: str = serializers.CharField(source="soort", default="")
    # contacts: List[GroupAdminContact] = GroupAdminContactSerializer(source="contacten", many=True, default=[])
    # links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, default=[])

    class Meta:
        model = ScoutsGroup
        fields = "__all__"

    def save(self) -> ScoutsGroup:
        return self.create(self.validated_data)

    def create(self, validated_data):
        instance = ScoutsGroup()

        address_serializer = GroupAdminAddressSerializer(validated_data.pop("addressen", []), many=True)
        address_serializer.is_valid(raise_exception=True)
        addresses = address_serializer.save()

        contact_serializer = GroupAdminContactSerializer(validated_data.pop("contacten", []), many=True)
        contact_serializer.is_valid(raise_exception=True)
        contacts = contact_serializer.save()

        link_serializer = GroupAdminLinkSerializer(validated_data.pop("links", []), many=True)
        link_serializer.is_valid(raise_exception=True)
        links = link_serializer.save()

        instance.group_admin_id = validated_data.pop("id", "")
        instance.number = validated_data.pop("groepsnummer", "")
        instance.name = validated_data.pop("naam", "")
        instance.addresses = addresses
        instance.date_of_foundation = validated_data.pop("opgericht", "")
        instance.only_leaders = validated_data.pop("enkelLeiding", False)
        instance.show_member_improved = validated_data.pop("ledenVerbeterdTonen", False)
        instance.bank_account = validated_data.pop("rekeningnummer", "")
        instance.email = validated_data.pop("email", "")
        instance.website = validated_data.pop("website", "")
        instance.info = validated_data.pop("vrijeInfo", "")
        instance.type = validated_data.pop("soort", "")
        instance.contacts = contacts
        instance.links = links

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
