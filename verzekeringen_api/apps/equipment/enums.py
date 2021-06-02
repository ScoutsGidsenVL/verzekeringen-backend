from django.db import models


class VehicleType(models.TextChoices):
    PASSENGER_CAR = "Personenwagen", "Personenwagen (maximum 5 passagiers)"
    MINIBUS = "Minibus", "Minibus (maximum 8 passagiers)"
    TRUCK = "Vrachtwagen tot 3.5 ton", "Vrachtwagen tot 3.5 ton (maximum 8 passagiers)"
