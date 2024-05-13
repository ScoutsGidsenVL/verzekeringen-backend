from django.db import models


class ClaimActivityType(models.TextChoices):
    REGULAR_ACTIVITY = "REGULAR", "regular activity"
    IRREGULAR_LOCATION = "IRREGULAR_LOCATION", "activity on another location"
    TRANSPORT = "TRANSPORT", "transport"
    OTHER = "OTHER", "other"
