from rest_framework import serializers

from scouts_insurances.equipment.models import VehicleType

from scouts_auth.inuits.models.fields import OptionalCharField


class VehicleSerializer(serializers.Serializer):
    type = OptionalCharField(choices=VehicleType.choices, max_length=30)
    brand = OptionalCharField()
    license_plate = OptionalCharField()
    construction_year = OptionalCharField()
    chassis_number = OptionalCharField()
    trailer = OptionalCharField()
