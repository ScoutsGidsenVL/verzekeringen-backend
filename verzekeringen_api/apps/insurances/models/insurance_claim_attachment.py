import logging

from apps.insurances.models import InsuranceClaim
from django.db import models
from scouts_auth.inuits.models import AbstractBaseModel, PersistedFile

logger = logging.getLogger(__name__)


class InsuranceClaimAttachment(AbstractBaseModel):
    file = models.OneToOneField(PersistedFile, on_delete=models.CASCADE, related_name="insurance_claim")
    insurance_claim = models.OneToOneField(InsuranceClaim, on_delete=models.CASCADE, related_name="attachment")
