import logging

from groupadmin.models import ScoutsFunction
from groupadmin.serializers import ScoutsLinkSerializer, ScoutsGroupSerializer, ScoutsGroupingSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsFunctionSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "type": data.pop("type", None),
            "group": ScoutsGroupSerializer().to_internal_value({"id": data.pop("groep", None)}),
            "function": data.pop("functie", None),
            "groups": ScoutsGroupSerializer(many=True).to_internal_value(
                [{"id": group} for group in data.pop("groepen", [])]
            ),
            "groupings": ScoutsGroupingSerializer(many=True).to_internal_value(data.pop("groeperingen", [])),
            "begin": data.pop("begin", None),
            "end": data.pop("einde", None),
            "max_birth_date": data.pop("uiterstegeboortedatum", None),
            "code": data.pop("code", None),
            "description": data.pop("omschrijving", data.pop("beschrijving", None)),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> ScoutsFunction:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsFunction:
        if validated_data is None:
            return None

        instance = ScoutsFunction()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.type = validated_data.pop("type", None)
        instance.group = ScoutsGroupSerializer().create(validated_data.pop("group", None))
        instance.function = validated_data.pop("function", "")
        instance.groups = ScoutsGroupSerializer(many=True).create(validated_data.pop("groups", []))
        instance.groupings = ScoutsGroupingSerializer(many=True).create(validated_data.pop("groupings", []))
        instance.begin = validated_data.pop("begin", None)
        instance.end = validated_data.pop("end", None)
        instance.max_birth_date = validated_data.pop("max_birth_date", None)
        instance.code = validated_data.pop("code", None)
        instance.description = validated_data.pop("description", "")
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
