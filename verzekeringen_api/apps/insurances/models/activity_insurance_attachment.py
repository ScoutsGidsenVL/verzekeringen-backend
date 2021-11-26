import logging

from django.db import models

from scouts_insurances.insurances.models import ActivityInsurance

from inuits.models import AbstractBaseModel, PersistedFile


logger = logging.getLogger(__name__)


class ActivityInsuranceAttachment(AbstractBaseModel):
    file = models.OneToOneField(PersistedFile, on_delete=models.CASCADE, related_name="activity_insurance")
    insurance = models.OneToOneField(ActivityInsurance, on_delete=models.CASCADE, related_name="attachment")
