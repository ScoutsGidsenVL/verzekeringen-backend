import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import GroupAdminAddress

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class GroupAdminAddressSerializer(NonModelSerializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "id": data.pop("id", ""),
            "street": data.pop("straat", ""),
            "number": data.pop("nummer", ""),
            "letter_box": data.pop("bus", ""),
            "postal_code": data.pop("postcode", ""),
            "city": data.pop("gemeente", ""),
            "country": data.pop("land", ""),
            "phone": data.pop("telefoon", ""),
            "postal_address": data.pop("postadres", False),
            "status": data.pop("status", ""),
            "position": data.pop("positie", ""),
            "giscode": data.pop("giscode", ""),
            "description": data.pop("omschrijving", ""),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> GroupAdminAddress:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminAddress:
        instance = GroupAdminAddress()

        instance.group_admin_id = validated_data.pop("id", "")
        instance.street = validated_data.pop("street", "")
        instance.number = validated_data.pop("number", "")
        instance.letter_box = validated_data.pop("letter_box", "")
        instance.postal_code = validated_data.pop("postal_code", "")
        instance.city = validated_data.pop("city", "")
        instance.country = validated_data.pop("country", "")
        instance.phone = validated_data.pop("phone", "")
        instance.postal_address = validated_data.pop("postal_address", False)
        instance.status = validated_data.pop("status", "")
        instance.position = validated_data.pop("position", "")
        instance.giscode = validated_data.pop("giscode", "")
        instance.description = validated_data.pop("description", "")

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
