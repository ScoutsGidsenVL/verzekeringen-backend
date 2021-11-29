import logging

from scouts_auth.groupadmin.models import ScoutsGroupListResponse
from scouts_auth.groupadmin.serializers import ScoutsLinkSerializer, ScoutsGroupSerializer, ScoutsResponseSerializer


logger = logging.getLogger(__name__)


class ScoutsGroupListResponseSerializer(ScoutsResponseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "scouts_groups": ScoutsGroupSerializer(many=True).to_internal_value(data.pop("groepen", [])),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def create(self, validated_data: dict) -> ScoutsGroupListResponse:
        if validated_data is None:
            return None

        instance = ScoutsGroupListResponse()

        instance.scouts_groups = ScoutsGroupSerializer(many=True).create(validated_data.pop("scouts_groups", []))
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
