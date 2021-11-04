import logging
from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import (
    GroupAdminMember,
    Gender,
    GenderHelper,
    GroupAdminAddress,
    GroupAdminContact,
    GroupAdminLink,
    ScoutsFunction,
)
from scouts_auth.serializers import (
    GroupAdminAddressSerializer,
    GroupAdminContactSerializer,
    GroupAdminLinkSerializer,
    ScoutsFunctionSerializer,
)


logger = logging.getLogger(__name__)


class GroupAdminMemberPersonalDataSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        validated_data: dict = {"gender": data.pop("geslacht", ""), "phone": data.pop("gsm", "")}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data


class GroupAdminMemberGroupAdminDataserializer(serializers.BaseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        validated_data: dict = {
            "first_name": data.pop("voornaam", ""),
            "last_name": data.pop("achternaam", ""),
            "birth_date": data.pop("geboortedatum", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data


class GroupAdminMemberScoutsDataSerializer(serializers.BaseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        validated_data: dict = {
            "membership_number": data.pop("lidnummer", ""),
            "customer_number": data.pop("klantnummer", ""),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data


class GroupAdminMemberSerializer(serializers.BaseSerializer):

    # gender: Gender = None
    # phone_number: str = serializers.CharField(source="gsm", required=False)
    # personal_data: dict = serializers.DictField(source="persoonsgegevens", default={})
    # groupadmin_data: dict = serializers.DictField(source="vgagegevens", default={})
    # scouts_data: dict = serializers.DictField(source="verbondsgegevens", default={})
    # email: str = serializers.CharField(default="")
    # username: str = serializers.CharField(source="gebruikersnaam", default="")
    # group_admin_id: str = serializers.CharField(source="id", default="")
    addresses: List[GroupAdminAddress] = GroupAdminAddressSerializer(source="addressen", many=True, default=[])
    contacts: List[GroupAdminContact] = GroupAdminContactSerializer(source="contacten", many=True, default=[])
    functions: List[ScoutsFunction] = ScoutsFunctionSerializer(source="functies", many=True, default=[])
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, default=[])

    def to_internal_value(self, data: dict) -> dict:
        validated_data: dict = {
            "group_admin_id": data.pop("id", ""),
            "gender": data.pop("id", ""),
            "phone_number": data.pop("groepsnummer", ""),
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

    def save(self) -> GroupAdminMember:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminMember:
        logger.debug("SERIALIZER CREATE -> validated_data: %s", validated_data)
        instance: GroupAdminMember = GroupAdminMember()
        logger.debug("KEYS: %d", len(validated_data.keys()))
        for key in self.validated_data.keys():
            logger.debug("%s: %s", key, validated_data.get(key))

        personal_data = validated_data.pop("persoonsgegevens", {})
        groupadmin_data = validated_data.pop("vgagegevens", {})
        scouts_data = validated_data.pop("verbondsgegevens", {})

        address_serializer = GroupAdminAddressSerializer(data=validated_data.pop("addressen", []), many=True)
        address_serializer.is_valid(raise_exception=True)
        addresses: List[GroupAdminAddress] = address_serializer.save()

        contact_serializer = GroupAdminContactSerializer(data=validated_data.pop("contacten", []), many=True)
        contact_serializer.is_valid(raise_exception=True)
        contacts: List[GroupAdminContact] = contact_serializer.save()

        function_serializer = ScoutsFunctionSerializer(data=validated_data.pop("functies", []), many=True)
        function_serializer.is_valid(raise_exception=True)
        functions: List[ScoutsFunction] = function_serializer.save()

        links_serializer = GroupAdminLinkSerializer(data=validated_data.pop("links", []), many=True)
        links_serializer.is_valid(raise_exception=True)
        links: List[GroupAdminLink] = links_serializer.save()

        instance.gender = GenderHelper.parse_gender(personal_data.pop("geslacht", ""))
        instance.phone_number = personal_data.pop("gsm", "")
        instance.first_name = groupadmin_data.pop("voornaam", "")
        instance.last_name = groupadmin_data.pop("achternaam", "")
        instance.birth_date = groupadmin_data.pop("geboortedatum", None)
        instance.membership_number = scouts_data.pop("lidnummer", "")
        instance.customer_number = scouts_data.pop("klantnummer", "")
        instance.email = validated_data.pop("email", "")
        instance.username = validated_data.pop("gebruikersnaam", "")
        instance.group_admin_id = validated_data.pop("id", "")
        instance.addresses = addresses
        instance.contacts = contacts
        instance.functions = functions
        instance.links = links

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
