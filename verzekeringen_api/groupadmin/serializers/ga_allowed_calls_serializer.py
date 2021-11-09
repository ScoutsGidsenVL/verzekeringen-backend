import logging

from groupadmin.models import ScoutsAllowedCalls
from groupadmin.serializers import ScoutsLinkSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsAllowedCallsSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {"links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", []))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsAllowedCalls:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsAllowedCalls:
        if validated_data is None:
            return None

        instance = ScoutsAllowedCalls()

        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
