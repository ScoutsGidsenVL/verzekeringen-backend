from django.db import models

from scouts_insurances.people.models import NonMember
from scouts_insurances.insurances.models import BaseInsurance, VehicleRelatedInsurance


class TravelAssistanceInsurance(VehicleRelatedInsurance, BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="travel_assistance_child",
    )
    country = models.CharField(db_column="bestemmingsland", max_length=40)

    # Even though this is an insurance only for members the participants are saved in the NonMember table
    # Cant change this because external database
    participants = models.ManyToManyField(
        NonMember, through="ParticipantTravelAssistanceInsurance", related_name="travel_assistance_insurances"
    )

    class Meta:
        db_table = "vrzktypeethiasassistance"
        managed = False

    # @property
    # def country(self):
    #     return Country.objects.get(name=self.country)

    # @country.setter
    # def country(self, value: Country):
    #     self.country = value.name
