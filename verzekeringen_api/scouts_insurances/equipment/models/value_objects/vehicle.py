# from django.db import models
# from django.core.validators import MinValueValidator

from scouts_insurances.equipment.models.enums import VehicleType, VehicleTrailerOption

# from scouts_auth.inuits.models.fields import (
#     OptionalCharField,
#     DefaultCharField,
#     RequiredCharField,
#     OptionalIntegerField,
# )


class Vehicle:
    DEFAULT_VEHICLE_TYPE = VehicleType.PASSENGER_CAR
    DEFAULT_VEHICLE_TRAILER_OPTION = VehicleTrailerOption.NO_TRAILER

    id: str
    type: VehicleType
    brand: str
    license_plate: str
    construction_year: int
    chassis_number: str
    trailer: VehicleTrailerOption

    def __init__(
        self,
        id: str = None,
        type: VehicleType = None,
        brand: str = "",
        license_plate: str = "",
        construction_year: int = None,
        chassis_number: str = "",
        trailer: VehicleTrailerOption = None,
    ):
        self.id = id
        self.type = type if type else self.DEFAULT_VEHICLE_TYPE
        self.brand = brand
        self.license_plate = license_plate
        self.construction_year = construction_year
        self.chassis_number = chassis_number
        self.trailer = trailer if trailer else self.DEFAULT_VEHICLE_TRAILER_OPTION

    def __str__(self):
        return "id({}), type({}), brand({}), license_plate({}), construction_year({}), chassis_number({}), trailer({})".format(
            self.id,
            self.type,
            self.brand,
            self.license_plate,
            self.construction_year,
            self.chassis_number,
            self.trailer,
        )
