import logging

from groupadmin.models import ScoutsValue

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsValueSerializer(NonModelSerializer):
    def to_internal_value(self, data: tuple) -> dict:
        if data is None:
            return None

        if data and len(data) == 2:
            (key, value) = data
            validated_data = {"key": key, "value": value}
        else:
            validated_data = {}

        return validated_data

    def save(self) -> ScoutsValue:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsValue:
        if validated_data is None:
            return None

        instance = ScoutsValue()

        instance.key = validated_data.pop("key", None)
        instance.value = validated_data.pop("value", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance