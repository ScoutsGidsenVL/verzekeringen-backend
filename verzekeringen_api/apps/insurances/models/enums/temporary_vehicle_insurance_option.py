from django.db import models


class TemporaryVehicleInsuranceOption(models.IntegerChoices):
    OMNIUM = 1, "omnium"
    COVER_OMNIUM = 2, "reeds afgesloten omnium afdekken"
    RENTAL = 3, "huurvoertuigen"
    OMNIUM_RENTAL = 13, "omnium + huurvoertuigen"
    COVER_OMNIUM_RENTAL = 23, "reeds afgesloten omnium afdekken + huurvoertuigen"
