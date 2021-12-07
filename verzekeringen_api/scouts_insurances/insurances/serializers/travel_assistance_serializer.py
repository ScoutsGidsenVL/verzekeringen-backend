import logging

from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from scouts_insurances.people.serializers import NonMemberSerializer
from scouts_insurances.locations.models import Country

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class TravelAssistanceInsuranceSerializer(BaseInsuranceSerializer):
    participants = NonMemberSerializer(many=True)
    vehicle = serializers.SerializerMethodField()
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.by_insurance_type_id(InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE),
        required=False,
    )

    class Meta:
        model = TravelAssistanceInsurance
        fields = BaseInsuranceFields + ["country", "participants", "vehicle", "group_admin_id", "scouts_group"]

    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        return value
