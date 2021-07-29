from django.db import models


class ActivityType(models.TextChoices):
    REGULAR_ACTIVITY = "REGULAR", "regular activity"
    IRREGULAR_LOCATION = "IRREGULAR_LOCATION", "activity on another location"
    TRANSPORT = "TRANSPORT", "transport"
    OTHER = "OTHER", "other"


class DamageType(models.TextChoices):
    GLASSES = "GLASSES", "glasses"
    MATERIAL = "MATERIAL", "material"
