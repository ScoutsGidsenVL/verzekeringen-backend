from django.db import models


class TemporaryVehicleParticipantType(models.TextChoices):
    DRIVER = "Bestuurder", "Bestuurder"
    OWNER = "Eigenaar", "Eigenaar"
