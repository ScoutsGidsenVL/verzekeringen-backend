from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from apps.scouts_auth.api.serializers import GroupOutputSerializer
from apps.members.api.serializers import (
    MemberNestedOutputSerializer,
    MemberNestedCreateInputSerializer,
    NonMemberNestedOutputSerializer,
    NonMemberCreateInputSerializer,
    BelgianPostcodeCityOutputSerializer,
    BelgianPostcodeCityInputSerializer,
)
from apps.equipment.api.serializers import VehicleOutputSerializer, VehicleInputSerializer
from .insurance_type_serializers import InsuranceTypeOutputSerializer
from ...models import BaseInsurance, ActivityInsurance, TemporaryInsurance, TravelAssistanceInsurance, InsuranceType
from ...models.enums import InsuranceStatus, GroupSize


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


class BaseInsuranceDetailOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    group = GroupOutputSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data


class ActivityInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    location = BelgianPostcodeCityOutputSerializer(source="postcode_city")
    group_size = serializers.SerializerMethodField()

    class Meta:
        model = ActivityInsurance
        fields = base_insurance_detail_fields + ("nature", "group_size", "location")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_group_size(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(GroupSize(obj.group_size))).data


class TemporaryInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    postcode_city = BelgianPostcodeCityOutputSerializer()
    non_members = NonMemberNestedOutputSerializer(many=True)

    class Meta:
        model = TemporaryInsurance
        fields = base_insurance_detail_fields + ("nature", "country", "postcode_city", "non_members")


class TravelAssistanceInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    participants = NonMemberNestedOutputSerializer(many=True)
    vehicle = VehicleOutputSerializer(read_only=True)

    class Meta:
        model = TravelAssistanceInsurance
        fields = base_insurance_detail_fields + ("country", "participants", "vehicle")


# Input
class BaseInsuranceCreateInputSerializer(serializers.Serializer):
    group = serializers.CharField(source="group_id", max_length=6)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    responsible_phone_number = serializers.CharField(max_length=15, required=False)


class ActivityInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    group_size = serializers.ChoiceField(choices=GroupSize.choices)
    location = BelgianPostcodeCityInputSerializer()


class TemporaryInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    country = serializers.CharField(max_length=45, required=False)
    postcode_city = BelgianPostcodeCityInputSerializer(required=False)
    non_members = NonMemberCreateInputSerializer(many=True)

    def validate_non_members(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one non member is required")
        return value

    def validate(self, data):
        if not data.get("postcode_city") and not data.get("country"):
            raise serializers.ValidationError("Either postcode_city or country is required")
        elif data.get("postcode_city") and data.get("country"):
            raise serializers.ValidationError("Country and postcode_city are mutually exclusive fields")
        return data


class TravelAssistanceInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    country = serializers.CharField(max_length=40)
    vehicle = VehicleInputSerializer(required=False)
    participants = NonMemberCreateInputSerializer(many=True)

    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        return value
