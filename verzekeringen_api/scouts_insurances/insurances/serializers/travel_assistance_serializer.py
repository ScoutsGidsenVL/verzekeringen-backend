import logging

from rest_framework import serializers

from scouts_insurances.equipment.serializers import VehicleSerializer
from scouts_insurances.people.serializers import NonMemberSerializer
from scouts_insurances.locations.models import Country
from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer


logger = logging.getLogger(__name__)


class TravelAssistanceInsuranceSerializer(BaseInsuranceSerializer):
    participants = NonMemberSerializer(many=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.by_insurance_type_id(InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE),
        required=False,
    )
    vehicle = VehicleSerializer()

    class Meta:
        model = TravelAssistanceInsurance
        fields = BaseInsuranceFields + ["country", "participants", "vehicle", "group_admin_id", "scouts_group"]

    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        return value
