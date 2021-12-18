from django.db import models

from scouts_insurances.people.models import NonMember
from scouts_insurances.insurances.models import BaseInsurance, VehicleWithTrailerRelatedInsurance
from scouts_insurances.insurances.models.enums import (
    TemporaryVehicleInsuranceCoverageOption,
    TemporaryVehicleInsuranceOption,
    TemporaryVehicleParticipantType,
)


class TemporaryVehicleInsurance(VehicleWithTrailerRelatedInsurance, BaseInsurance):

    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="temporary_vehicle_child",
    )
    insurance_options = models.IntegerField(db_column="keuze", choices=TemporaryVehicleInsuranceOption.choices)
    max_coverage = models.CharField(
        db_column="maxdekking",
        choices=TemporaryVehicleInsuranceCoverageOption.choices,
        max_length=1,
        null=True,
        blank=True,
    )

    # Even though this is an insurance only for members the participants are saved in the NonMember table
    # Cant change this because external database
    participants = models.ManyToManyField(
        NonMember, through="ParticipantTemporaryVehicleInsurance", related_name="temporary_vehicle_insurances"
    )

    class Meta:
        db_table = "vrzktypetijdauto"
        managed = False

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

    # @property
    # def insurance_options(self):
    #     return [int(digit) for digit in str(self._insurance_option)]

    # @insurance_options.setter
    # def insurance_options(self, value: set):
    #     print("INSURANCE OPTIONS ", value)
    #     self._insurance_option = int("".join([str(sub_value) for sub_value in value]))
