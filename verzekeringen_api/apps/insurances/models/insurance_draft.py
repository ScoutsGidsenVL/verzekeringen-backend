from django.db import models

from apps.insurances.managers import InsuranceDraftManager
from scouts_auth.inuits.models import AuditedBaseModel
from scouts_insurances.insurances.models import InsuranceType


class InsuranceDraft(AuditedBaseModel):
    """Stores intermediate work on insurance requests."""

    objects = InsuranceDraftManager()

    data = models.JSONField()
    insurance_type = models.ForeignKey(InsuranceType, related_name="insurance_drafts", on_delete=models.RESTRICT)
