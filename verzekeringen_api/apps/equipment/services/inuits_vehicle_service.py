from django.conf import settings
from django.db import transaction

from apps.equipment.models import InuitsVehicle


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
    def inuits_vehicle_update(self, *, vehicle: InuitsVehicle, updated_vehicle: InuitsVehicle) -> InuitsVehicle:
        vehicle.type = updated_vehicle.type
        vehicle.brand = updated_vehicle.brand
        vehicle.license_plate = updated_vehicle.license_plate
        vehicle.construction_year = updated_vehicle.construction_year
        vehicle.chassis_number = updated_vehicle.chassis_number
        vehicle.trailer = updated_vehicle.trailer

        vehicle.full_clean()
        vehicle.save()

        return vehicle
