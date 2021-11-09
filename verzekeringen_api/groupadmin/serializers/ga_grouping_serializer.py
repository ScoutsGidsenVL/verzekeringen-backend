import logging

from groupadmin.models import ScoutsGrouping

from inuits.serializers import NonModelSerializer

logger = logging.getLogger(__name__)


class ScoutsGroupingSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {"name": data.pop("naam", None), "index": data.pop("volgorde", None)}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsGrouping:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsGrouping:
        if validated_data is None:
            return None

        instance = ScoutsGrouping()

        instance.name = validated_data.pop("name", None)
        instance.index = validated_data.pop("index", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
