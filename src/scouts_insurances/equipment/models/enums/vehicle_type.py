from django.db import models


class VehicleType(models.TextChoices):
    PASSENGER_CAR = "PERSONENWAGEN", "Personenwagen (max. 4+1 inzittenden)"
    MINIBUS = "MINIBUS", "Minibus (max. 8+1 inzittenden)"
    TRUCK = "VRACHTWAGEN", "Lichte vrachtauto tot 3,5 ton (max. 8+1 inzittenden)"

    @staticmethod
    def from_choice(choice: str):
        for vehicle_type in VehicleType.choices:
            if vehicle_type[0] == choice:
                return vehicle_type
        return None
