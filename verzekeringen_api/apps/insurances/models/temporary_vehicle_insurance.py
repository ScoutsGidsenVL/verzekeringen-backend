from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator

from apps.members.models import NonMember
from apps.equipment.utils import Vehicle
from apps.equipment.enums import VehicleType, VehicleTrailerOption
from apps.insurances.models.enums import (
    TemporaryVehicleInsuranceCoverageOption,
    TemporaryVehicleInsuranceOption,
    TemporaryVehicleParticipantType,
)
from apps.insurances.models.base_insurance import BaseInsurance


class TemporaryVehicleInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="temporary_vehicle_child",
    )
    _insurance_option = models.IntegerField(db_column="keuze", choices=TemporaryVehicleInsuranceOption.choices)
    max_coverage = models.CharField(
        db_column="maxdekking",
        choices=TemporaryVehicleInsuranceCoverageOption.choices,
        max_length=1,
        null=True,
        blank=True,
    )
    _vehicle_type = models.CharField(
        db_column="autotype", choices=VehicleType.choices, max_length=30, null=True, blank=True
    )
    _vehicle_brand = models.CharField(db_column="automerk", max_length=15, null=True, blank=True)
    _vehicle_license_plate = models.CharField(db_column="autokenteken", max_length=10, null=True, blank=True)
    _vehicle_construction_year = models.IntegerField(
        db_column="autobouwjaar", null=True, blank=True, validators=[MinValueValidator(1900)]
    )
    _vehicle_chassis_number = models.CharField(db_column="autochassis", max_length=20)
    _vehicle_trailer = models.CharField(
        db_column="aanhangwagen", choices=VehicleTrailerOption.choices, max_length=1, default="0"
    )

    # Even though this is an insurance only for members the participants are saved in the NonMember table
    # Cant change this because external database
    participants = models.ManyToManyField(
        NonMember, through="ParticipantTemporaryVehicleInsurance", related_name="temporary_vehicle_insurances"
    )

    class Meta:
        db_table = "vrzktypetijdauto"
        managed = False

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
            raise ValidationError("If one vehicle field given all vehicle fields need to be given")

    # Handle vehicle using seperate class so we can reuse it in other insurances
    @property
    def vehicle(self):
        # If no vehicle type all other fields are empty aswell
        if not self._vehicle_type:
            return None
        return Vehicle(
            type=VehicleType(self._vehicle_type),
            brand=self._vehicle_brand,
            license_plate=self._vehicle_license_plate,
            construction_year=datetime.strptime(str(self._vehicle_construction_year), "%Y").date(),
            chassis_number=self._vehicle_chassis_number,
            trailer=self._vehicle_trailer,
        )

    @vehicle.setter
    def vehicle(self, value: Vehicle):
        self._vehicle_type = value.type.value
        self._vehicle_brand = value.brand
        self._vehicle_license_plate = value.license_plate
        self._vehicle_construction_year = value.construction_year.year
        self._vehicle_chassis_number = value.chassis_number
        self._vehicle_trailer = value.trailer

    @property
    def owner(self):
        return self.insurance_participants.get(type=TemporaryVehicleParticipantType.OWNER).participant

    @property
    def drivers(self):
        return [
            insurance_participant.participant
            for insurance_participant in self.insurance_participants.filter(
                type=TemporaryVehicleParticipantType.DRIVER
            )
        ]

    @property
    def insurance_options(self):
        return [int(digit) for digit in str(self._insurance_option)]

    @insurance_options.setter
    def insurance_options(self, value: set):
        self._insurance_option = int("".join([str(sub_value) for sub_value in value]))


class ParticipantTemporaryVehicleInsurance(models.Model):
    participant = models.ForeignKey(
        NonMember,
        db_column="bestuurderid",
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="temporary_vehicle",
    )
    insurance = models.ForeignKey(
        TemporaryVehicleInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        related_name="insurance_participants",
    )

    type = models.CharField(db_column="soort", choices=TemporaryVehicleParticipantType.choices, max_length=10)

    class Meta:
        db_table = "vrzktijdautonietleden"
        managed = False
