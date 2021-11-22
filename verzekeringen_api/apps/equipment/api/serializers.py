from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from apps.members.api.serializers import (
    InuitsNonMemberOutputSerializer,
    MemberNestedOutputSerializer,
    NonMemberNestedOutputSerializer,
    MemberNestedCreateInputSerializer,
    NonMemberCreateInputSerializer,
)
from apps.members.models import InuitsNonMember
from apps.equipment.models import InuitsVehicle, InuitsEquipment, Equipment, VehicleInuitsTemplate
from apps.equipment.enums import VehicleType, VehicleTrailerOption
from apps.equipment.utils import Vehicle

from groupadmin.serializers import ScoutsMemberSearchFrontendSerializer
from groupadmin.services import GroupAdmin


# Output
class VehicleOutputSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField()
    brand = serializers.CharField()
    license_plate = serializers.CharField()
    construction_year = serializers.DateField(format="%Y")
    trailer = serializers.SerializerMethodField()
    inuits_vehicle_id = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_inuits_vehicle_id(self, obj) -> bool:
        inuits_vehicle_template = VehicleInuitsTemplate.objects.filter(
            temporary_vehicle_insurance=self.context.get("id")
        ).first()
        print(inuits_vehicle_template)
        if inuits_vehicle_template:
            return inuits_vehicle_template.inuits_vehicle.id

        return None

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(VehicleType(obj.type))).data

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_trailer(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(VehicleTrailerOption(obj.trailer))).data


class VehicleWithChassisOutputSerializer(VehicleOutputSerializer):
    chassis_number = serializers.CharField()
    trailer = serializers.SerializerMethodField()

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_trailer(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(VehicleTrailerOption(obj.trailer))).data


class InuitsVehicleOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()
    trailer = serializers.SerializerMethodField()

    class Meta:
        model = InuitsVehicle
        fields = (
            "id",
            "type",
            "brand",
            "license_plate",
            "construction_year",
            "chassis_number",
            "trailer",
        )

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(VehicleType(obj.type))).data

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_trailer(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(VehicleTrailerOption(obj.trailer))).data


class EquipmentNestedOutputSerializer(serializers.ModelSerializer):
    owner_non_member = NonMemberNestedOutputSerializer()
    owner_member = MemberNestedOutputSerializer()

    class Meta:
        model = Equipment
        fields = (
            "id",
            "nature",
            "description",
            "total_value",
            "owner_non_member",
            "owner_member",
        )


class InuitsEquipmentListOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InuitsEquipment
        fields = (
            "id",
            "nature",
            "description",
            "total_value",
            "group_group_admin_id",
        )


class InuitsEquipmentDetailOutputSerializer(serializers.ModelSerializer):
    owner_non_member = InuitsNonMemberOutputSerializer()
    owner_member = serializers.SerializerMethodField()

    class Meta:
        model = InuitsEquipment
        fields = (
            "id",
            "nature",
            "description",
            "total_value",
            "owner_non_member",
            "owner_member",
            "group_group_admin_id",
        )

    @swagger_serializer_method(serializer_or_field=ScoutsMemberSearchFrontendSerializer)
    def get_owner_member(self, obj):
        if not obj.owner_member_group_admin_id:
            return None
        request = self.context.get("request", None)
        return ScoutsMemberSearchFrontendSerializer(
            GroupAdmin().get_member_info(active_user=request.user, group_admin_id=obj.owner_member_group_admin_id)
        ).data


# Input
class VehicleInputSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=VehicleType.choices)
    brand = serializers.CharField(max_length=15)
    license_plate = serializers.CharField(max_length=10)
    construction_year = serializers.DateField(input_formats=["%Y"])
    chassis_number = serializers.CharField(max_length=20, required=False, allow_null=True)
    trailer = serializers.ChoiceField(choices=VehicleTrailerOption.choices, required=False)
    inuits_vehicle_id = serializers.CharField(max_length=36, required=False, allow_blank=True)

    def validate(self, data):
        return Vehicle(
            type=VehicleType(data.get("type")),
            brand=data.get("brand"),
            license_plate=data.get("license_plate"),
            construction_year=data.get("construction_year"),
            chassis_number=data.get("chassis_number"),
            trailer=data.get("trailer", False),
            inuits_vehicle_id=data.get("inuits_vehicle_id", None),
        )


class VehicleWithChassisInputSerializer(VehicleInputSerializer):
    chassis_number = serializers.CharField(max_length=20, required=True)


class InuitsVehicleCreateInputSerializer(VehicleInputSerializer):
    group_group_admin_id = serializers.CharField()

    def validate(self, data):
        return data


class EquipmentInputSerializer(serializers.Serializer):
    nature = serializers.CharField(max_length=50, required=False, allow_null=True)
    description = serializers.CharField(max_length=500)
    total_value = serializers.DecimalField(max_digits=7, decimal_places=2)
    owner_member = MemberNestedCreateInputSerializer(required=False)
    owner_non_member = NonMemberCreateInputSerializer(required=False)

    def validate(self, data):
        if data.get("owner_member") and data.get("owner_non_member"):
            raise serializers.ValidationError("There can only be one max owner")
        return data


class InuitsEquipmentCreateInputSerializer(EquipmentInputSerializer):
    # Special filter field so we can get allowed in queryset
    class InuitsEquipmentNonMemberRelatedField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            request = self.context.get("request", None)
            queryset = InuitsNonMember.objects.all().allowed(request.user)
            return queryset

    group_group_admin_id = serializers.CharField(source="group_group_admin_id")
    owner_member = serializers.CharField(source="owner_member_id", required=False, allow_null=True)
    owner_non_member = InuitsEquipmentNonMemberRelatedField(required=False, allow_null=True)

    def validate_owner_member(self, value):
        # Validate wether membership number of member is valid
        request = self.context.get("request", None)
        try:
            if value:
                GroupAdmin().get_member_info(active_user=request.user, group_admin_id=value)
        except:
            raise serializers.ValidationError("Invalid member id given")
        return value

    def validate(self, data):
        if data.get("owner_member_id") and data.get("owner_non_member"):
            raise serializers.ValidationError("There can only be one max owner")
        return data
