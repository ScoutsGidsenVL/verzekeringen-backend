from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from apps.scouts_auth.api.serializers import GroupOutputSerializer
from apps.members.api.serializers import (
    MemberNestedOutputSerializer,
    MemberNestedCreateInputSerializer,
    BelgianPostcodeCityOutputSerializer,
    BelgianPostcodeCityInputSerializer,
)
from apps.members.utils import PostcodeCity
from .insurance_type_serializers import InsuranceTypeOutputSerializer
from ...models import BaseInsurance, ActivityInsurance, InsuranceType
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


# Just some a tuple so we dont need to copy everything (cannot use inheritance because Meta does not get inherited)
base_insurance_detail_fields = (
    "id",
    "status",
    "type",
    "group",
    "start_date",
    "end_date",
    "responsible_member",
    "total_cost",
    "created_on",
    "comment",
    "vvks_comment",
)


class ActivityInsuranceDetailOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    group = GroupOutputSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)
    location = serializers.SerializerMethodField()

    class Meta:
        model = ActivityInsurance
        fields = base_insurance_detail_fields + ("nature", "group_amount", "location")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data

    @swagger_serializer_method(serializer_or_field=BelgianPostcodeCityOutputSerializer)
    def get_location(self, obj):
        return BelgianPostcodeCityOutputSerializer(PostcodeCity(postcode=obj.postcode, name=obj.city)).data


# Input
class BaseInsuranceCreateInputSerializer(serializers.Serializer):
    group = serializers.CharField(source="group_id", max_length=6)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    responsible_phone_number = serializers.CharField(max_length=15, required=False)


class ActivityInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    group_amount = serializers.IntegerField(min_value=1, max_value=9)
    location = BelgianPostcodeCityInputSerializer()
