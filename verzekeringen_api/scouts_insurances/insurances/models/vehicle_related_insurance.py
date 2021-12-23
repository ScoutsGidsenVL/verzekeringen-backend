from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from rest_framework import serializers

from scouts_insurances.equipment.models import Vehicle
from scouts_insurances.equipment.models.enums import VehicleType

from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    OptionalIntegerField,
)


class VehicleRelatedInsurance(models.Model):

    _vehicle_type = OptionalCharField(
        db_column="autotype",
        choices=VehicleType.choices,
        # default=Vehicle.DEFAULT_VEHICLE_TYPE,
        max_length=30,
    )
    _vehicle_brand = OptionalCharField(db_column="automerk", max_length=15)
    _vehicle_license_plate = OptionalCharField(db_column="autokenteken", max_length=10)
    _vehicle_construction_year = OptionalIntegerField(db_column="autobouwjaar", validators=[MinValueValidator(1900)])
    _vehicle_chassis_number = OptionalCharField(db_column="autochassis", max_length=20)

    class Meta:
        abstract = True

    def clean(self):
        super().clean()
        if not (
            self._vehicle_type
            and self._vehicle_brand
            and self._vehicle_license_plate
            and self._vehicle_construction_year
        ) and not (
            not self._vehicle_type
            and not self._vehicle_brand
            and not self._vehicle_license_plate
            and not self._vehicle_construction_year
        ):
            raise serializers.ValidationError("If one vehicle field given all vehicle fields need to be given")

    # Handle vehicle using seperate class so we can reuse it in other insurances
    def get_vehicle(self) -> Vehicle:
        # If no vehicle type all other fields are empty aswell
        if not self._vehicle_type:
            return None

        return Vehicle(
            type=self._vehicle_type,
            brand=self._vehicle_brand,
            license_plate=self._vehicle_license_plate,
            construction_year=self._vehicle_construction_year,
            chassis_number=self._vehicle_chassis_number,
        )

    def set_vehicle(self, obj: Vehicle = None):
        self._vehicle_type = None
        self._vehicle_brand = None
        self._vehicle_license_plate = None
        self._vehicle_construction_year = None
        self._vehicle_chassis_number = None

        if not obj:
            return

        self._vehicle_type = obj.type
        self._vehicle_brand = obj.brand
        self._vehicle_license_plate = obj.license_plate
        self._vehicle_construction_year = obj.construction_year
        self._vehicle_chassis_number = obj.chassis_number

    def clean_construction_year(self, value):
        if datetime.strptime("1900", "%Y") > value:
            raise ValidationError("Invalid construction year")
        return value

    def __str__(self):
        return self.vehicle_to_str()

    def vehicle_to_str(self):
        return "type({}), brand({}), license_plate({}), construction_year({}), chassis_number({})".format(
            self._vehicle_type,
            self._vehicle_brand,
            self._vehicle_license_plate,
            self._vehicle_construction_year,
            self._vehicle_chassis_number,
        )
