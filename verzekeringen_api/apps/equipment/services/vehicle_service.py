from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from ..models import InuitsVehicle


def inuits_vehicle_create(
    *,
    type: str,
    brand: str,
    license_plate: str,
    construction_year: datetime.date,
    chassis_number: str,
    group_id: str,
    created_by: settings.AUTH_USER_MODEL,
    trailer: bool = False,
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
