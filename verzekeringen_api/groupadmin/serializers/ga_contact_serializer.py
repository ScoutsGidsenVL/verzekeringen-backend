import logging

from groupadmin.models import ScoutsContact
from groupadmin.serializers import ScoutsLinkSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsContactSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "member": data.pop("oidLid", data.pop("lid", None)),
            "function": data.pop("oidFunctie", data.pop("functie", None)),
            "name": data.pop("naam", None),
            "phone_number": data.pop("tel", None),
            "email": data.pop("email", None),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsContact:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsContact:
        if validated_data is None:
            return None

        instance = ScoutsContact()

        instance.member = validated_data.pop("member", None)
        instance.function = validated_data.pop("function", None)
        instance.name = validated_data.pop("name", None)
        instance.phone_number = validated_data.pop("phone_number", None)
        instance.email = validated_data.pop("email", None)
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance