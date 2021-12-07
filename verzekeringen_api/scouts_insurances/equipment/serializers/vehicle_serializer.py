import logging

from rest_framework import serializers

from scouts_insurances.equipment.models import Vehicle, VehicleType, VehicleTrailerOption
from scouts_insurances.insurances.models import VehicleRelatedInsurance

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_auth.inuits.serializers.fields import OptionalCharField, ChoiceSerializerField


logger = logging.getLogger(__name__)


class VehicleSerializer(serializers.Serializer):
    # @TODO This is hacky and should not be here, as it refers to the InuitsVehicle id
    id = serializers.UUIDField(required=False)
    type = ChoiceSerializerField(choices=VehicleType.choices, default=Vehicle.DEFAULT_VEHICLE_TYPE)
    brand = OptionalCharField()
    license_plate = OptionalCharField()
    construction_year = OptionalCharField()
    chassis_number = OptionalCharField()
    trailer = ChoiceSerializerField(choices=VehicleTrailerOption, default=Vehicle.DEFAULT_VEHICLE_TRAILER_OPTION)

    class Meta:
        model = Vehicle
        fields = "__all__"

    def to_internal_value(self, data: dict) -> Vehicle:
        super().to_internal_value(data)

        return Vehicle(
            type=data.get("type", Vehicle.DEFAULT_VEHICLE_TYPE),
            brand=data.get("brand", ""),
            license_plate=data.get("license_plate", ""),
            construction_year=data.get("construction_year", None),
            chassis_number=data.get("chassis_number", None),
            trailer=data.get("trailer", Vehicle.DEFAULT_VEHICLE_TRAILER_OPTION),
        )

    def to_representation(self, obj: Vehicle) -> dict:
        data = super().to_representation(obj)

        data["type"] = EnumSerializer((obj.type.value, obj.type.label)).data
        data["trailer"] = EnumSerializer((obj.trailer.value, obj.trailer.label)).data

        return data
