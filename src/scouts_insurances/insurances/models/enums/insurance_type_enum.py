from django.db import models


class InsuranceTypeEnum(models.IntegerChoices):
    ACTIVITY = 1
    TEMPORARY = 2
    TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE = 3
    TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE = 4
    TEMPORARY_VEHICLE = 5
    EQUIPMENT = 6
    EVENT = 10

    @staticmethod
    def parse_type(type: int):
        if not type:
            return None

        # to be sure, to be sure
        type = int(type)

        for choice in InsuranceTypeEnum.choices:
            if choice[0] == type:
                return choice

        return None
