import logging
from typing import List

from groupadmin.models import ScoutsGroupSpecificField
from groupadmin.serializers import ScoutsValueSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsGroupSpecificFieldSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> list:
        if data is None:
            return None

        validated_data = []
        groups = data.keys()

        for group in groups:
            group_data: dict = data.get(group, None)
            validated = {}

            validated["scouts_group"] = group
            validated["schema"] = group_data.pop("schema", None)
            # validated["values"] = ScoutsValueSerializer().to_internal_value(group_data.pop("waarden", {}))

            validated_data.append(validated)

        return validated_data

    def save(self) -> ScoutsGroupSpecificField:
        return self.create(self.validated_data)

    def create(self, validated_data: list) -> List[ScoutsGroupSpecificField]:
        if validated_data is None:
            return None

        fields = []
        for data in validated_data:
            instance = ScoutsGroupSpecificField()

            instance.scouts_group = data.pop("scouts_group", None)
            instance.schema = data.pop("schema", None)
            # instance.values = ScoutsValueSerializer().create(data.pop("values", {}))

            fields.append(instance)

        return fields
