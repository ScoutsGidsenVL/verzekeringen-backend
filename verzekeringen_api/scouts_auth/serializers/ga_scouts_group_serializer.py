import logging
from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import GroupAdminContact, ScoutsGroup, GroupAdminLink, GroupAdminAddress
from scouts_auth.serializers import GroupAdminLinkSerializer, GroupAdminAddressSerializer, GroupAdminContactSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsGroupSerializer(NonModelSerializer):
    """Serializes a Group instance to a string."""

    def to_internal_value(self, data: dict) -> dict:
        validated_data: dict = {
            "group_admin_id": data.pop("id", ""),
            "number": data.pop("groepsnummer", ""),
            "name": data.pop("naam", ""),
            "date_of_foundation": data.pop("opgericht", None),
            "bank_account": data.pop("rekeningnummer", ""),
            "email": data.pop("email", ""),
            "website": data.pop("website", ""),
            "info": data.pop("vrijeInfo", ""),
            "type": data.pop("soort", ""),
            "only_leaders": bool(data.pop("enkelLeiding", False)),
            "show_members_improved": bool(data.pop("ledenVerbeterdTonen", False)),
            "addresses": GroupAdminAddressSerializer(many=True).to_internal_value(data.pop("adressen", [])),
            "contacts": GroupAdminContactSerializer(many=True).to_internal_value(data.pop("contacten", [])),
            "links": GroupAdminLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsGroup:
        return self.create(self.validated_data)

    def create(self, validated_data) -> ScoutsGroup:
        instance = ScoutsGroup()

        instance.group_admin_id = validated_data.pop("group_admin_id", "")
        instance.number = validated_data.pop("number", "")
        instance.name = validated_data.pop("name", "")
        instance.date_of_foundation = validated_data.pop("date_of_foundation", "")
        instance.bank_account = validated_data.pop("bank_account", "")
        instance.email = validated_data.pop("email", "")
        instance.website = validated_data.pop("website", "")
        instance.info = validated_data.pop("info", "")
        instance.type = validated_data.pop("type", "")
        instance.only_leaders = validated_data.pop("only_leaders", False)
        instance.show_members_improved = validated_data.pop("show_members_improved", False)
        instance.addresses = GroupAdminAddressSerializer(many=True).create(validated_data.pop("addresses", []))
        instance.contacts = GroupAdminContactSerializer(many=True).create(validated_data.pop("contacts", []))
        instance.links = GroupAdminLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
