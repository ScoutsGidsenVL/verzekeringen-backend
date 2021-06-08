from django.db import models


class TemporaryVehicleInsuranceCoverageOption(models.TextChoices):
    A = "A", "247,89 EUR"
    B = "B", "495,79 EUR"
    C = "C", "743,68 EUR"
