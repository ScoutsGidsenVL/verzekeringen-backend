import logging

from rest_framework import serializers

from apps.equipment.models import InuitsVehicle, InuitsVehicleTrailerOption
from scouts_auth.inuits.serializers import EnumSerializer
from scouts_auth.inuits.serializers.fields import ChoiceSerializerField
from scouts_insurances.equipment.models import VehicleType

logger = logging.getLogger(__name__)


class InuitsVehicleSerializer(serializers.ModelSerializer):
    # id                pk
    # type              max_length=30       optional        VehicleType.choices
    # brand             max_length=15       optional
    # license_plate     max_length=10       optional
    # construction_year minimum 1900        optional
    # chassis_number    max_length=20       required
    # trailer           max_length=1        default="0"     VehicleTrailerOption.choices

    class Meta:
        model = InuitsVehicle
        fields = "__all__"

    # def to_internal_value(self, data) -> InuitsVehicle:
    #     # @TODO fix trailer option
    #     vehicle = TemporaryVehicleInsuranceVehicle(**super().to_internal_value(data))

    #     logger.debug("VEHICLE: %s", vehicle)

    #     return InuitsVehicle.from_vehicle(vehicle)
    def to_internal_value(self, data: dict) -> InuitsVehicle:
        # @TODO remove group_group_admin_id from frontend serializer
        # logger.debug("DATA: %s", data)
        data.pop("group_group_admin_id", None)
        # logger.debug("DATA: %s", data)
        # return InuitsVehicle(**data)
        return data

    def to_representation(self, obj: InuitsVehicle) -> dict:
        type = VehicleType.from_choice(obj.type)
        trailer = InuitsVehicleTrailerOption.from_choice(obj.trailer)

        data = super().to_representation(obj)

        logger.debug("VEHICLE OBJECT TO REPRESENT: %s", obj)

        logger.debug("VEHICLE TYPE: %s", type)
        data["type"] = EnumSerializer((type[0], type[1])).data

        logger.debug("VEHICLE TRAILER: %s", trailer)
        data["trailer"] = EnumSerializer((trailer[0], trailer[1])).data

        return data

    def validate(self, data: dict) -> InuitsVehicle:
        return InuitsVehicle(**data)
