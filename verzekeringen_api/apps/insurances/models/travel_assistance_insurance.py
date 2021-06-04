from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.members.models import NonMember
from apps.equipment.utils import Vehicle
from apps.equipment.enums import VehicleType
from apps.locations.models import Country
from .base_insurance import BaseInsurance


class TravelAssistanceInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="travel_assistance_child",
    )
    _country = models.CharField(db_column="bestemmingsland", max_length=40)
    _vehicle_type = models.CharField(db_column="autotype", max_length=30, null=True, blank=True)
    _vehicle_brand = models.CharField(db_column="automerk", max_length=15, null=True, blank=True)
    _vehicle_license_plate = models.CharField(db_column="autokenteken", max_length=10, null=True, blank=True)
    _vehicle_construction_year = models.IntegerField(
        db_column="autobouwjaar", null=True, blank=True, validators=[MinValueValidator(1900)]
    )
    _vehicle_trailer = models.IntegerField(
        db_column="aanhangwagen",
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    # Even though this is an insurance only for members the participants are saved in the NonMember table
    # Cant change this because external database
    participants = models.ManyToManyField(
        NonMember, through="ParticipantTravelAssistanceInsurance", related_name="travel_assistance_insurances"
    )

    class Meta:
        db_table = "vrzktypeethiasassistance"
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
            chassis_number="",
            trailer=bool(self._vehicle_trailer),
        )

    @vehicle.setter
    def vehicle(self, value: Vehicle):
        self._vehicle_type = value.type.value
        self._vehicle_brand = value.brand
        self._vehicle_license_plate = value.license_plate
        self._vehicle_construction_year = value.construction_year.year
        self._vehicle_trailer = int(value.trailer)

    @property
    def country(self):
        return Country.objects.get(name=self._country)

    @country.setter
    def country(self, value: Country):
        self._country = value.name


class ParticipantTravelAssistanceInsurance(models.Model):
    participant = models.ForeignKey(NonMember, db_column="passagierid", on_delete=models.CASCADE, primary_key=True)
    temporary_insurance = models.ForeignKey(
        TravelAssistanceInsurance, db_column="verzekeringsid", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "vrzkassistpassagier"
        managed = False
