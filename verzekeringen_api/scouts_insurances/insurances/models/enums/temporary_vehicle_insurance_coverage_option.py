from django.db import models


class TemporaryVehicleInsuranceCoverageOption(models.TextChoices):
    A = "A", "247,89 EUR"
    B = "B", "495,79 EUR"
    C = "C", "743,68 EUR"

    @staticmethod
    def from_choice(choice: str):
        for option in TemporaryVehicleInsuranceCoverageOption.choices:
            if option[0] == choice:
                return option
        return None
