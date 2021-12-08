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
    vehicle = VehicleSerializer()
    participants = NonMemberSerializer(many=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.by_insurance_type_id(InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE),
        required=False,
    )

    class Meta:
        model = TravelAssistanceInsurance
        fields = BaseInsuranceFields + ["country", "participants", "vehicle", "group_admin_id", "scouts_group"]

    def to_internal_value(self, data: dict) -> dict:
        vehicle = data.pop("vehicle", None)

        data = super().to_internal_value(data)

        if vehicle:
            vehicle_serializer = VehicleSerializer(data=vehicle)
            vehicle_serializer.is_valid(raise_exception=True)

            # Travel assistance vehicles don't care for the type of trailer
            serialized_vehicle = vehicle_serializer.validated_data
            serialized_vehicle.trailer = 1 if serialized_vehicle.trailer != 0 else 0

            data["vehicle"] = serialized_vehicle

        return data

    def validate(self, data: dict) -> dict:
        participants = data.get("participants", [])
        if len(participants) < 1:
            raise serializers.ValidationError("At least one participant is required")

        return data
