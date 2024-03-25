from django.db import models
from rest_framework import serializers

from scouts_insurances.insurances.models import BaseInsurance, VehicleWithSimpleTrailerRelatedInsurance
from scouts_insurances.people.models import NonMember


class TravelAssistanceInsurance(VehicleWithSimpleTrailerRelatedInsurance, BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="travel_assistance_child",
    )
    country = models.CharField(db_column="bestemmingsland", max_length=60)

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
            raise serializers.ValidationError("If one vehicle field given all vehicle fields need to be given")
