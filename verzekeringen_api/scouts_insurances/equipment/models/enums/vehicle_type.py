from django.db import models


class VehicleType(models.TextChoices):
    PASSENGER_CAR = "PERSONENWAGEN", "Personenwagen (maximum 5 inzittenden)"
    MINIBUS = "MINIBUS", "Minibus (maximum 8 inzittenden)"
    TRUCK = "VRACHTWAGEN", "Vrachtwagen tot 3.5 ton (maximum 8 inzittenden)"
