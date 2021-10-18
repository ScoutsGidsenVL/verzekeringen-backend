import logging

from django.db import models

from apps.insurances.models import InsuranceClaim
from inuits.files.validators import validate_file_extension
from inuits.models import BaseModel


logger = logging.getLogger(__name__)


class InsuranceClaimAttachment(BaseModel):
    file = models.FileField(
        validators=[validate_file_extension],
        null=True,
        blank=True,
    )
    content_type = models.CharField(max_length=100)
    insurance_claim = models.OneToOneField(
        InsuranceClaim, on_delete=models.CASCADE, related_name="attachment", null=True
    )
