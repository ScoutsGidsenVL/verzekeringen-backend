from django.db import models


class VehicleTrailerOption(models.TextChoices):
    NO_TRAILER = "0", "Geen"
    TRAILER_LESS_750 = "2", "<750kg"
    TRAILER_MORE_750 = "3", ">750kg"
