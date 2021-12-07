from datetime import datetime

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.equipment.models import InuitsVehicle

from scouts_insurances.equipment.models import VehicleTrailerOption


class InuitsVehicleService:
    @transaction.atomic
    def inuits_vehicle_create(
        self,
        #     *,
        #     type: str,
        #     brand: str,
        #     license_plate: str,
        #     construction_year: datetime.date,
        #     chassis_number: str,
        #     created_by: settings.AUTH_USER_MODEL,
        #     trailer: str = VehicleTrailerOption.NO_TRAILER,
        inuits_vehicle: InuitsVehicle,
        created_by: settings.AUTH_USER_MODEL,
    ) -> InuitsVehicle:
        # vehicle = InuitsVehicle(
        #     type=type,
        #     brand=brand,
        #     license_plate=license_plate,
        #     construction_year=construction_year,
        #     chassis_number=chassis_number,
        #     trailer=trailer,
        # )
        inuits_vehicle.full_clean()
        inuits_vehicle.save()

        return inuits_vehicle

    @transaction.atomic
    def inuits_vehicle_update(self, *, vehicle: InuitsVehicle, **fields) -> InuitsVehicle:
        vehicle.type = fields.get("type", vehicle.type)
        vehicle.brand = fields.get("brand", vehicle.brand)
        vehicle.license_plate = fields.get("license_plate", vehicle.license_plate)
        vehicle.construction_year = fields.get("construction_year", vehicle.construction_year)
        vehicle.chassis_number = fields.get("chassis_number", vehicle.chassis_number)
        vehicle.trailer = fields.get("trailer", vehicle.trailer)

        vehicle.full_clean()
        vehicle.save()

        return vehicle
