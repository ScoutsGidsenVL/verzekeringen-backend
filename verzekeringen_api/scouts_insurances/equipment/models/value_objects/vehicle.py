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


# class Vehicle(models.Model):
#     type = DefaultCharField(
#         db_column="autotype",
#         choices=VehicleType.choices,
#         default="VehicleRelatedInsurance.DEFAULT_VEHICLE_TYPE",
#         max_length=30,
#     )
#     brand = OptionalCharField(db_column="automerk", max_length=15)
#     license_plate = OptionalCharField(db_column="autokenteken", max_length=10)
#     construction_year = OptionalIntegerField(db_column="autobouwjaar", validators=[MinValueValidator(1900)])
#     chassis_number = RequiredCharField(db_column="autochassis", max_length=20, default=None)
#     trailer = DefaultCharField(
#         db_column="aanhangwagen",
#         choices=VehicleTrailerOption.choices,
#         max_length=1,
#         default="VehicleRelatedInsurance.DEFAULT_VEHICLE_TRAILER_OPTION",
#     )

#     class Meta:
#         abstract = True
