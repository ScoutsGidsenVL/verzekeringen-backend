import logging

from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from inuits.serializers import EnumSerializer, DateTimeTimezoneField
from inuits.filters.helpers import parse_choice_to_tuple

from scouts_insurances.people.serializers import MemberSerializer
from scouts_insurances.insurances.models.enums import InsuranceStatus
from scouts_insurances.insurances.serializers import InsuranceTypeSerializer

from groupadmin.serializers import ScoutsGroupSerializer


logger = logging.getLogger(__name__)


class BaseInsuranceSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeSerializer(read_only=True)
    scouts_group = ScoutsGroupSerializer(read_only=True)
    responsible_member = MemberSerializer(read_only=True)
    start_date = DateTimeTimezoneField()
    end_date = DateTimeTimezoneField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    vvks_comment = serializers.CharField(max_length=500, required=False, allow_blank=True)

    @swagger_serializer_method(serializer_or_field=EnumSerializer)
    def get_status(self, obj):
        return EnumSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data
