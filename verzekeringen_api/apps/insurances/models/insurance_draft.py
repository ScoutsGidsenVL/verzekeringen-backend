from django.db import models

from apps.insurances.managers import InsuranceDraftManager

from scouts_insurances.insurances.models import InsuranceType

from inuits.models import AuditedBaseModel


class InsuranceDraft(AuditedBaseModel):
    """Stores intermediate work on insurance requests."""

    objects = InsuranceDraftManager()

    id = models.AutoField(primary_key=True)
    data = models.JSONField()
    insurance_type = models.ForeignKey(InsuranceType, related_name="insurance_drafts", on_delete=models.RESTRICT)
