from apps.equipment.managers import InuitsVehicleManager

from scouts_insurances.equipment.models import Vehicle

from scouts_auth.inuits.models import AbstractBaseModel


class InuitsVehicle(Vehicle, AbstractBaseModel):
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
