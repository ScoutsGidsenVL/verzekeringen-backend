from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.equipment.managers import InuitsVehicleManager

from scouts_insurances.equipment.models import VehicleType, VehicleTrailerOption

from scouts_auth.inuits.models.fields import OptionalCharField, RequiredCharField, OptionalIntegerField


class InuitsVehicle(models.Model):
    """
    Extra vehicle class we can use to save and search unique vehicles.

    The scouts insurance representation of a vehicle is kept in the TemporaryVehicleInsurance table,
    together with the insurance reference. There is no separate entity.
    This class provides a way of doing CRUD with at least some of the data filled in if the vehicle
    exists in the scouts insurance table.

    Differences with the vehicle in TemporaryVehicleInsurance:
    - (chassis_number,license_plate, trailer) is unique

    The jointable is defined in InuitVehicleTemplate
    """

    objects = InuitsVehicleManager()

    inuits_vehicle_id = models.AutoField(primary_key=True)
    type = OptionalCharField(choices=VehicleType.choices, max_length=30)
    brand = OptionalCharField(max_length=15)
    license_plate = OptionalCharField(max_length=10)
    construction_year = OptionalIntegerField(validators=[MinValueValidator(1900)])
    chassis_number = RequiredCharField(max_length=20)
    trailer = models.CharField(choices=VehicleTrailerOption.choices, max_length=1, default="0")

    # class Meta:
    #     unique_together = ["chassis_number", "license_plate", "trailer"]

    def clean_construction_year(self, value):
        if datetime.strptime("1900", "%Y") > value:
            raise ValidationError("Invalid construction year")
        return value
