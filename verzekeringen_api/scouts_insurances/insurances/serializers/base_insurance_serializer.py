import logging

from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from scouts_auth.inuits.serializers import EnumSerializer, DateTimeTimezoneField
from scouts_auth.inuits.filters.helpers import parse_choice_to_tuple

from scouts_insurances.people.serializers import MemberSerializer
from scouts_insurances.insurances.models import BaseInsurance
from scouts_insurances.insurances.models.enums import InsuranceStatus
from scouts_insurances.insurances.serializers import InsuranceTypeSerializer

from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer


logger = logging.getLogger(__name__)


class BaseInsuranceSerializer(serializers.ModelSerializer):
    # id                    pk
    # status                number          optional
    # scouts_group          ScoutsGroup
    # total_cost            decimal         optional
    # comment               max_length=500  optional
    # vvksm_comment         max_length=500  optional
    # created_on            datetime        optional
    # start_date            datetime        optional
    # end_date              datetime        optional
    # responsible_member    Member          required
    # type                  InsuranceType   optional

    class Meta:
        model = BaseInsurance
        fields = "__all__"

    @swagger_serializer_method(serializer_or_field=EnumSerializer)
    def get_status(self, obj):
        return EnumSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data
