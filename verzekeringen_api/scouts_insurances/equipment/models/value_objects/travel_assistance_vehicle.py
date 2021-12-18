from scouts_insurances.equipment.models.value_objects import Vehicle
from scouts_insurances.equipment.models.enums import VehicleType, TravelAssistanceVehicleTrailerOption


class TravelAssistanceVehicle(Vehicle):

    DEFAULT_VEHICLE_TRAILER_OPTION = TravelAssistanceVehicleTrailerOption.NO_TRAILER

    trailer: TravelAssistanceVehicleTrailerOption = None

    def __init__(
        self,
        id: str = None,
        type: VehicleType = None,
        brand: str = "",
        license_plate: str = "",
        construction_year: int = None,
        chassis_number: str = "",
        trailer: TravelAssistanceVehicleTrailerOption = None,
    ):
        super().__init__(id, type, brand, license_plate, construction_year, chassis_number)

        self.trailer = trailer if trailer else self.DEFAULT_VEHICLE_TRAILER_OPTION

    def __str__(self):
        return super().__str__() + ", trailer({})".format(self.trailer)
