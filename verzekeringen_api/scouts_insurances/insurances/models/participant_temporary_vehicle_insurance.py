from django.db import models

from scouts_insurances.people.models import NonMember
from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.models.enums import TemporaryVehicleParticipantType


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
