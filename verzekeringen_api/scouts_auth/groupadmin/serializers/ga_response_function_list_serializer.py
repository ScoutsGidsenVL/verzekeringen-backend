import logging

from scouts_auth.groupadmin.models import ScoutsFunctionListResponse
from scouts_auth.groupadmin.serializers import ScoutsLinkSerializer, ScoutsFunctionSerializer, ScoutsResponseSerializer


logger = logging.getLogger(__name__)


class ScoutsFunctionListResponseSerializer(ScoutsResponseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "functions": ScoutsFunctionSerializer(many=True).to_internal_value(data.pop("functies", [])),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsFunctionListResponse:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsFunctionListResponse:
        if validated_data is None:
            return None

        instance = ScoutsFunctionListResponse()

        instance.functions = ScoutsFunctionSerializer(many=True).create(validated_data.pop("functions", []))
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
