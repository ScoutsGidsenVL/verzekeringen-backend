from scouts_insurances.equipment.models.enums import TemporaryVehicleInsuranceVehicleTrailerOption, VehicleType
from scouts_insurances.equipment.models.value_objects import Vehicle


class TemporaryVehicleInsuranceVehicle(Vehicle):

    DEFAULT_VEHICLE_TRAILER_OPTION = TemporaryVehicleInsuranceVehicleTrailerOption.NO_TRAILER

    trailer: TemporaryVehicleInsuranceVehicleTrailerOption = None

    def __init__(
        self,
        id: str = None,
        type: VehicleType = None,
        brand: str = "",
        license_plate: str = "",
        construction_year: int = None,
        chassis_number: str = "",
        trailer: TemporaryVehicleInsuranceVehicleTrailerOption = None,
    ):
        super().__init__(id, type, brand, license_plate, construction_year, chassis_number)

        self.trailer = trailer if trailer else self.DEFAULT_VEHICLE_TRAILER_OPTION

    def __str__(self):
        return super().__str__() + ", trailer({})".format(self.trailer)

    def vehicle_to_str_mail(self):
        return f"Type: {self.type.lower()}, Merk: {self.brand}, Nummerplaat: {self.license_plate}, Bouwjaar: {self.construction_year}, Chassisnummer: {self.chassis_number}, Aanhangwagen: {self.trailer.from_choice(self.trailer)[1]}"
