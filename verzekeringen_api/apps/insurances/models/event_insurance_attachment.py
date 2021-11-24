import logging

from django.conf import settings
from django.db import models

from apps.insurances.models import EventInsurance

from inuits.files.validators import validate_file_extension
from inuits.models import BaseModel


logger = logging.getLogger(__name__)


class EventInsuranceAttachment(BaseModel):
    file = models.FileField(
        validators=[validate_file_extension],
        null=True,
        blank=True,
    )
    content_type = models.CharField(max_length=100)
    event_insurance = models.OneToOneField(
        EventInsurance, on_delete=models.CASCADE, related_name="attachment", null=True
    )
