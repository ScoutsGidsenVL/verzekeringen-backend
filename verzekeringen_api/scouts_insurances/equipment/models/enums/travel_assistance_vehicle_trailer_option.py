from django.db import models


class TravelAssistanceVehicleTrailerOption(models.TextChoices):
    NO_TRAILER = "0", "Geen"
    TRAILER = "1", "Aanhangwagen"

    @staticmethod
    def from_choice(choice: str):
        choice = str(choice)
        # logger.debug("VEHICLE TRAILER CHOICE: %s", choice)
        for option in TravelAssistanceVehicleTrailerOption.choices:
            # logger.debug("VEHICLE TRAILER OPTION: %s", option)
            if option[0] == choice:
                # logger.debug("VEHICLE TRAILER OPTION CHOSEN: %s", option)
                return option
        return None
