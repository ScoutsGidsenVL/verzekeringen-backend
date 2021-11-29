import logging

from django.db import models

from scouts_insurances.insurances.models import EventInsurance

from scouts_auth.inuits.models import AbstractBaseModel, PersistedFile


logger = logging.getLogger(__name__)


class EventInsuranceAttachment(AbstractBaseModel):
    file = models.OneToOneField(PersistedFile, on_delete=models.CASCADE, related_name="event_insurance")
    insurance = models.OneToOneField(EventInsurance, on_delete=models.CASCADE, related_name="attachment", null=True)
