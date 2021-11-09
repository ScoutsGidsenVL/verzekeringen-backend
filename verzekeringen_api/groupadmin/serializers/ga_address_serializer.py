import logging

from groupadmin.models import ScoutsAddress
from groupadmin.serializers import ScoutsPositionSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsAddressSerializer(NonModelSerializer):
    def to_internal_value(self, data) -> dict:
        if data is None:
            return None

        validated_data = {
            "id": data.pop("id", None),
            "street": data.pop("straat", None),
            "number": data.pop("nummer", None),
            "letter_box": data.pop("bus", None),
            "postal_code": data.pop("postcode", None),
            "city": data.pop("gemeente", None),
            "country": data.pop("land", None),
            "phone": data.pop("telefoon", None),
            "postal_address": data.pop("postadres", None),
            "status": data.pop("status", None),
            "position": ScoutsPositionSerializer().to_internal_value(data.pop("positie", None)),
            "giscode": data.pop("giscode", None),
            "description": data.pop("omschrijving", None),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsAddress:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsAddress:
        if validated_data is None:
            return None

        instance = ScoutsAddress()

        instance.group_admin_id = validated_data.pop("id", None)
        instance.street = validated_data.pop("street", None)
        instance.number = validated_data.pop("number", None)
        instance.letter_box = validated_data.pop("letter_box", None)
        instance.postal_code = validated_data.pop("postal_code", None)
        instance.city = validated_data.pop("city", None)
        instance.country = validated_data.pop("country", None)
        instance.phone = validated_data.pop("phone", None)
        instance.postal_address = validated_data.pop("postal_address", None)
        instance.status = validated_data.pop("status", None)
        instance.position = ScoutsPositionSerializer().create(validated_data.pop("position", None))
        instance.giscode = validated_data.pop("giscode", None)
        instance.description = validated_data.pop("description", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
