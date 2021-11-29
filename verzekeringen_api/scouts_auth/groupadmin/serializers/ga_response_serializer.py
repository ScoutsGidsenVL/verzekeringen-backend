import logging

from scouts_auth.groupadmin.models import ScoutsResponse
from scouts_auth.groupadmin.serializers import ScoutsLinkSerializer

from scouts_auth.inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsResponseSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "count": data.pop("aantal", None),
            "total": data.pop("totaal", None),
            "offset": data.pop("offset", None),
            "filter_criterium": data.pop("filtercriterium", None),
            "criteria": data.pop("criteria", None),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        return validated_data

    def save(self) -> ScoutsResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsResponse:
        if validated_data is None:
            return None

        instance = ScoutsResponse()

        instance.count = validated_data.pop("count", None)
        instance.total = validated_data.pop("total", None)
        instance.offset = validated_data.pop("offset", None)
        instance.filter_criterium = validated_data.pop("filter_criterium", None)
        instance.criteria = validated_data.pop("criteria", None)
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        return instance

    def update(self, instance: ScoutsResponse, validated_data: dict) -> ScoutsResponse:
        instance.count = validated_data.pop("count", instance.count)
        instance.total = validated_data.pop("total", instance.total)
        instance.offset = validated_data.pop("offset", instance.offset)
        instance.filter_criterium = validated_data.pop("filter_criterium", instance.filter_criterium)
        instance.criteria = validated_data.pop("criteria", instance.criteria)
        instance.links = validated_data.pop("links", instance.links)

        return instance
