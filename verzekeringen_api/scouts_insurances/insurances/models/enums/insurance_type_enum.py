from django.db import models


class InsuranceTypeEnum(models.IntegerChoices):
    ACTIVITY = 1  # (TypeEenmaligeActiviteit)
    TEMPORARY = 2  # (TypeTijdelijkeVerzekering)
    TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE = 3  # (TypeEthiasAssistanceZonderAuto)
    TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE = 4  # (TypeEthiasAssistanceMetAuto)
    TEMPORARY_VEHICLE = 5  # (TypeTijdelijkeAutoverzekering)
    EQUIPMENT = 6  # (TypeGroepsmateriaalVerzekering)
    EVENT = 10  # (TypeEvenementenVerzekering)

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
