import logging

from apps.people.serializers import InuitsNonMemberSerializer

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.serializers import TravelAssistanceInsuranceSerializer


logger = logging.getLogger(__name__)


class InuitsTravelAssistanceInsuranceSerializer(TravelAssistanceInsuranceSerializer):
    participants = InuitsNonMemberSerializer(many=True)

    class Meta:
        model = TravelAssistanceInsurance
        fields = TravelAssistanceInsuranceSerializer.Meta.fields

    def to_internal_value(self, data: dict) -> dict:
        # logger.debug("DATA: %s", data)

        data = super().to_internal_value(data)

        # logger.debug("DATA: %s", data)

        return data
