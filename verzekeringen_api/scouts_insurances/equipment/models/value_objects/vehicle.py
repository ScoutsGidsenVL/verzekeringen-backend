from scouts_insurances.equipment.models.enums import VehicleType


class Vehicle:
    DEFAULT_VEHICLE_TYPE = VehicleType.PASSENGER_CAR

    id: str
    type: VehicleType
    brand: str
    license_plate: str
    construction_year: int
    chassis_number: str

    def __init__(
        self,
        id: str = None,
        type: VehicleType = None,
        brand: str = "",
        license_plate: str = "",
        construction_year: int = None,
        chassis_number: str = "",
    ):
        self.id = id
        self.type = type if type else self.DEFAULT_VEHICLE_TYPE
        self.brand = brand
        self.license_plate = license_plate
        self.construction_year = construction_year
        self.chassis_number = chassis_number

    def __str__(self):
        return "id({}), type({}), brand({}), license_plate({}), construction_year({}), chassis_number({})".format(
            self.id,
            self.type,
            self.brand,
            self.license_plate,
            self.construction_year,
            self.chassis_number,
        )
