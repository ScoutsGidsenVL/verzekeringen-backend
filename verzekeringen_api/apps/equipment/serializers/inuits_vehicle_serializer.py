import logging

from rest_framework import serializers

from apps.equipment.models import InuitsVehicle

from scouts_insurances.equipment.models import Vehicle
from scouts_insurances.equipment.serializers import VehicleSerializer


logger = logging.getLogger(__name__)


class InuitsVehicleSerializer(VehicleSerializer, serializers.ModelSerializer):
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

    def to_internal_value(self, data) -> InuitsVehicle:
        vehicle: Vehicle = super().to_internal_value(data)

        logger.debug("VEHICLE: %s", vehicle)

        return InuitsVehicle.from_vehicle(vehicle)
