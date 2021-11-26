from re import T
from rest_framework import serializers

from apps.equipment.models import InuitsVehicle


class InuitsVehicleSerializer(serializers.ModelSerializer):
    # inuits_vehicle_id pk
    # type              max_length=30       optional        VehicleType.choices
    # brand             max_length=15       optional
    # license_plate     max_length=10       optional
    # construction_year minimum 1900        optional
    # chassis_number    max_length=20       required
    # trailer           max_length=1        default="0"     VehicleTrailerOption.choices

    class Meta:
        model = InuitsVehicle
        fields = "__all__"
