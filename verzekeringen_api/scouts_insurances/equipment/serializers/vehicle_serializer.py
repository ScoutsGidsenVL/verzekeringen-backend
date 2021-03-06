import logging

from rest_framework import serializers

from scouts_insurances.equipment.models import Vehicle, VehicleType
from scouts_insurances.equipment.serializers.fields import VehicleTypeSerializerField

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_auth.inuits.serializers.fields import OptionalCharField


logger = logging.getLogger(__name__)


class VehicleSerializer(serializers.Serializer):
    # @TODO This is hacky and should not be here, as it refers to the InuitsVehicle id
    id = serializers.UUIDField(required=False)
    type = VehicleTypeSerializerField(default=Vehicle.DEFAULT_VEHICLE_TYPE)
    brand = OptionalCharField()
    license_plate = OptionalCharField()
    construction_year = OptionalCharField()
    chassis_number = OptionalCharField()

    class Meta:
        model = Vehicle
        fields = "__all__"

    # def to_internal_value(self, data: dict) -> Vehicle:
    #     super().to_internal_value(data)

    #     return Vehicle(
    #         type=VehicleType.from_choice(data.get("type", Vehicle.DEFAULT_VEHICLE_TYPE)),
    #         # type=data.get("type", Vehicle.DEFAULT_VEHICLE_TYPE),
    #         brand=data.get("brand", ""),
    #         license_plate=data.get("license_plate", ""),
    #         construction_year=data.get("construction_year", None),
    #         chassis_number=data.get("chassis_number", None),
    #     )

    # def to_representation(self, obj: Vehicle) -> dict:
    #     data = super().to_representation(obj)

    #     type = VehicleType.from_choice(obj.type)
    #     logger.debug("VEHICLE TYPE: %s", type)
    #     data["type"] = EnumSerializer((type[0], type[1])).data

    #     return data
