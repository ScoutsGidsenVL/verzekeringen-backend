from django.db import models


class ClaimDamageType(models.TextChoices):
    GLASSES = "GLASSES", "glasses"
    MATERIAL = "MATERIAL", "material"
