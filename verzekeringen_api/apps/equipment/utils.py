from datetime import datetime

from apps.equipment.enums import VehicleType, VehicleTrailerOption


class Vehicle:
    type: VehicleType
    brand: str
    license_plate: str
    construction_year: datetime.date
    chassis_number: str
    trailer: str
    inuits_vehicle_id: str

    def __init__(
        self,
        type,
        brand,
        license_plate,
        construction_year,
        chassis_number="",
        trailer=VehicleTrailerOption.NO_TRAILER,
        inuits_vehicle_id=None,
    ):
        self.type = type
        self.brand = brand
        self.license_plate = license_plate
        self.construction_year = construction_year
        self.chassis_number = chassis_number
        self.trailer = trailer
        self.inuits_vehicle_id = inuits_vehicle_id

    @property
    def has_trailer(self):
        return self.trailer != VehicleTrailerOption.NO_TRAILER

    @property
    def has_heavy_trailer(self):
        return self.trailer == VehicleTrailerOption.TRAILER_MORE_750
