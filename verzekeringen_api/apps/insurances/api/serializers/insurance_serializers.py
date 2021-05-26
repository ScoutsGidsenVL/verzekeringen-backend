from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from apps.scouts_auth.api.serializers import GroupOutputSerializer
from apps.members.api.serializers import (
    MemberNestedOutputSerializer,
    MemberNestedCreateInputSerializer,
)
from .insurance_type_serializers import InsuranceTypeOutputSerializer
from ...models import BaseInsurance, InsuranceType
from ...models.enums import InsuranceStatus


# Output
class InsuranceListOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    group = GroupOutputSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)

    class Meta:
        model = BaseInsurance
        fields = ("id", "status", "type", "group", "start_date", "end_date", "responsible_member")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data


# Input
class BaseInsuranceCreateInputSerializer(serializers.Serializer):
    group = serializers.CharField(source="group_id", max_length=6)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    responsible_phone_number = serializers.CharField(max_length=15, required=False)


class ActivityInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    people_amount = serializers.IntegerField(min_value=1, max_value=9)
    postcode = serializers.IntegerField()
    city = serializers.CharField(max_length=40)
