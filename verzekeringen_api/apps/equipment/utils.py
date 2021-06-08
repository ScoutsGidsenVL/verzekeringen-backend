from datetime import datetime
from .enums import VehicleType, VehicleTrailerOption


class Vehicle:
    type: VehicleType
    brand: str
    license_plate: str
    construction_year: datetime.date
    chassis_number: str
    trailer: str

    def __init__(
        self, type, brand, license_plate, construction_year, chassis_number="", trailer=VehicleTrailerOption.NO_TRAILER
    ):
        self.type = type
        self.brand = brand
        self.license_plate = license_plate
        self.construction_year = construction_year
        self.chassis_number = chassis_number
        self.trailer = trailer

    @property
    def has_trailer(self):
        return self.trailer != VehicleTrailerOption.NO_TRAILER
