from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from ..models import InuitsVehicle
from ..enums import VehicleType
from ..utils import Vehicle


# Output
class VehicleOutputSerializer(serializers.Serializer):
    type = serializers.SerializerMethodField()
    brand = serializers.CharField()
    license_plate = serializers.CharField()
    construction_year = serializers.DateField(format="%Y")
    trailer = serializers.BooleanField()

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_type(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(VehicleType(obj.type))).data


class VehicleWithChassisOutputSerializer(VehicleOutputSerializer):
    chassis_number = serializers.CharField()


class InuitsVehicleOutputSerializer(serializers.ModelSerializer):
    type = serializers.SerializerMethodField()

    class Meta:
        model = InuitsVehicle
        fields = (
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


# Input
class VehicleInputSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=VehicleType.choices)
    brand = serializers.CharField(max_length=15)
    license_plate = serializers.CharField(max_length=10)
    construction_year = serializers.DateField(input_formats=["%Y"])
    chassis_number = serializers.CharField(max_length=20)
    trailer = serializers.BooleanField(required=False)

    def validate(self, data):
        return Vehicle(
            type=VehicleType(data.get("type")),
            brand=data.get("brand"),
            license_plate=data.get("license_plate"),
            construction_year=data.get("construction_year"),
            chassis_number=data.get("chassis_number"),
            trailer=data.get("trailer", False),
        )


class InuitsVehicleCreateInputSerializer(VehicleInputSerializer):
    group = serializers.CharField(source="group_id")

    def validate(self, data):
        return data
