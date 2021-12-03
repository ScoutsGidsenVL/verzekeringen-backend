from django.db import models


class InsuranceTypeEnum(models.IntegerChoices):
    ACTIVITY = 1
    TEMPORARY = 2
    TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE = 3
    TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE = 4
    TEMPORARY_VEHICLE = 5
    EQUIPMENT = 6
    EVENT = 10
