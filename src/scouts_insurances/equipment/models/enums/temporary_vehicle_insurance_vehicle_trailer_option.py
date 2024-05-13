import logging

from django.db import models

logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceVehicleTrailerOption(models.TextChoices):
    NO_TRAILER = "0", "Geen"
    TRAILER_LESS_750 = "2", "<750kg"
    TRAILER_MORE_750 = "3", ">750kg"

    @staticmethod
    def from_choice(choice: str):
        choice = str(choice)
        # logger.debug("VEHICLE TRAILER CHOICE: %s", choice)
        for option in TemporaryVehicleInsuranceVehicleTrailerOption.choices:
            # logger.debug("VEHICLE TRAILER OPTION: %s", option)
            if option[0] == choice:
                # logger.debug("VEHICLE TRAILER OPTION CHOSEN: %s", option)
                return option
        return None
