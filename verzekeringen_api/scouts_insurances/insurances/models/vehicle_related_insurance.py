from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from scouts_insurances.equipment.models import Vehicle
from scouts_insurances.equipment.models.enums import VehicleType, VehicleTrailerOption

from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    DefaultCharField,
    OptionalIntegerField,
)


class VehicleRelatedInsurance(models.Model):

    _vehicle_type = OptionalCharField(
        db_column="autotype",
        choices=VehicleType.choices,
        default=Vehicle.DEFAULT_VEHICLE_TYPE,
        max_length=30,
    )
    _vehicle_brand = OptionalCharField(db_column="automerk", max_length=15)
    _vehicle_license_plate = OptionalCharField(db_column="autokenteken", max_length=10)
    _vehicle_construction_year = OptionalIntegerField(db_column="autobouwjaar", validators=[MinValueValidator(1900)])
    _vehicle_trailer = DefaultCharField(
        db_column="aanhangwagen",
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

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
    @property
    def vehicle(self) -> Vehicle:
        # If no vehicle type all other fields are empty aswell
        if not self._vehicle_type:
            return None

        return Vehicle(
            type=self._vehicle_type,
            brand=self._vehicle_brand,
            license_plate=self._vehicle_license_plate,
            construction_year=self._vehicle_construction_year,
            trailer=self._vehicle_trailer,
        )

    @vehicle.setter
    def vehicle(self, value: Vehicle):
        self._vehicle_type = value.type
        self._vehicle_brand = value.brand
        self._vehicle_license_plate = value.license_plate
        self._vehicle_construction_year = value.construction_year
        self._vehicle_trailer = value.trailer

    def clean_construction_year(self, value):
        if datetime.strptime("1900", "%Y") > value:
            raise ValidationError("Invalid construction year")
        return value

    @property
    def has_trailer(self):
        return self._vehicle_trailer != VehicleTrailerOption.NO_TRAILER

    @property
    def has_heavy_trailer(self):
        return self._vehicle_trailer == VehicleTrailerOption.TRAILER_MORE_750
