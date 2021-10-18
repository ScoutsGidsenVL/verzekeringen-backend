from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError

from apps.equipment.models import InuitsVehicle
from apps.equipment.utils import VehicleTrailerOption


def inuits_vehicle_create(
    *,
    type: str,
    brand: str,
    license_plate: str,
    construction_year: datetime.date,
    chassis_number: str,
    group_id: str,
    created_by: settings.AUTH_USER_MODEL,
    trailer: str = VehicleTrailerOption.NO_TRAILER,
) -> InuitsVehicle:
    # validate group
    if group_id not in (group.id for group in created_by.partial_scouts_groups):
        raise ValidationError("Given group %s is not a valid group of user" % group_id)
    vehicle = InuitsVehicle(
        type=type,
        brand=brand,
        license_plate=license_plate,
        construction_year=construction_year,
        chassis_number=chassis_number,
        group_number=group_id,
        trailer=trailer,
    )
    vehicle.full_clean()
    vehicle.save()

    return vehicle


def inuits_vehicle_update(*, vehicle: InuitsVehicle, **fields) -> InuitsVehicle:
    vehicle.type = fields.get("type", vehicle.type)
    vehicle.brand = fields.get("brand", vehicle.brand)
    vehicle.license_plate = fields.get("license_plate", vehicle.license_plate)
    vehicle.construction_year = fields.get("construction_year", vehicle.construction_year)
    vehicle.chassis_number = fields.get("chassis_number", vehicle.chassis_number)
    vehicle.trailer = fields.get("trailer", vehicle.trailer)

    vehicle.full_clean()
    vehicle.save()

    return vehicle
