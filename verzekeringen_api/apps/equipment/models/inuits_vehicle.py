import uuid

from django.core.validators import MinValueValidator

from apps.equipment.managers import InuitsVehicleManager

from scouts_insurances.equipment.models import Vehicle, VehicleType, VehicleTrailerOption

from scouts_auth.inuits.models import AbstractBaseModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    DefaultCharField,
    RequiredCharField,
    OptionalIntegerField,
)


class InuitsVehicle(AbstractBaseModel):
    """
    Extra vehicle class we can use to save and search unique vehicles.

    The scouts insurance representation of a vehicle is kept in the TemporaryVehicleInsurance table,
    together with the insurance reference. There is no separate entity.
    This class provides a way of doing CRUD with at least some of the data filled in if the vehicle
    exists in the scouts insurance table.

    Differences with the vehicle in TemporaryVehicleInsurance:
    - (chassis_number,license_plate, trailer) is unique

    The jointable is defined in InuitVehicleTemplate
    """

    objects = InuitsVehicleManager()

    type = DefaultCharField(
        db_column="autotype",
        choices=VehicleType.choices,
        default="VehicleRelatedInsurance.DEFAULT_VEHICLE_TYPE",
        max_length=30,
    )
    brand = OptionalCharField(db_column="automerk", max_length=15)
    license_plate = OptionalCharField(db_column="autokenteken", max_length=10)
    construction_year = OptionalIntegerField(db_column="autobouwjaar", validators=[MinValueValidator(1900)])
    chassis_number = RequiredCharField(db_column="autochassis", max_length=20, default=None)
    trailer = DefaultCharField(
        db_column="aanhangwagen",
        choices=VehicleTrailerOption.choices,
        max_length=1,
        default="VehicleRelatedInsurance.DEFAULT_VEHICLE_TRAILER_OPTION",
    )

    @staticmethod
    def from_vehicle(vehicle: Vehicle):
        return InuitsVehicle(
            id=vehicle.id,
            type=vehicle.type,
            brand=vehicle.brand,
            license_plate=vehicle.license_plate,
            construction_year=vehicle.construction_year,
            chassis_number=vehicle.chassis_number,
            trailer=vehicle.trailer,
        )

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
