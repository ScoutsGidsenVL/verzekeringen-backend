from django.db import models

from scouts_insurances.people.models import NonMember
from scouts_insurances.insurances.models import TravelAssistanceInsurance


class ParticipantTravelAssistanceInsurance(models.Model):
    participant = models.ForeignKey(
        NonMember, db_column="passagierid", on_delete=models.CASCADE, primary_key=True, related_name="travel"
    )
    temporary_insurance = models.ForeignKey(
        TravelAssistanceInsurance, db_column="verzekeringsid", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "vrzkassistpassagier"
        managed = False
