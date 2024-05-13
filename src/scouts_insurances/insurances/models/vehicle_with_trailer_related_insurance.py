from scouts_auth.inuits.models.fields import OptionalCharField
from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicle
from scouts_insurances.equipment.models.enums import TemporaryVehicleInsuranceVehicleTrailerOption
from scouts_insurances.insurances.models import VehicleRelatedInsurance


class VehicleWithTrailerRelatedInsurance(VehicleRelatedInsurance):

    _vehicle_trailer = OptionalCharField(
        db_column="aanhangwagen",
        choices=TemporaryVehicleInsuranceVehicleTrailerOption.choices,
        max_length=1,
        # default=TemporaryVehicleInsuranceVehicle.DEFAULT_VEHICLE_TRAILER_OPTION,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True

    # Handle vehicle using seperate class so we can reuse it in other insurances
    @property
    def vehicle(self) -> TemporaryVehicleInsuranceVehicle:
        # If no vehicle type all other fields are empty aswell
        if not self.get_vehicle():
            return None

        return TemporaryVehicleInsuranceVehicle(
            id=self._vehicle_id,
            type=self._vehicle_type,
            brand=self._vehicle_brand,
            license_plate=self._vehicle_license_plate,
            construction_year=self._vehicle_construction_year,
            chassis_number=self._vehicle_chassis_number,
            trailer=self._vehicle_trailer,
        )

    @vehicle.setter
    def vehicle(self, obj: TemporaryVehicleInsuranceVehicle = None):
        self._vehicle_trailer = None
        self._vehicle_id = None

        super().set_vehicle(obj)

        if obj:
            self._vehicle_trailer = obj.trailer
            self._vehicle_id = obj.id

    @property
    def has_trailer(self):
        return self._vehicle_trailer != TemporaryVehicleInsuranceVehicleTrailerOption.NO_TRAILER

    @property
    def has_heavy_trailer(self):
        return self._vehicle_trailer == TemporaryVehicleInsuranceVehicleTrailerOption.TRAILER_MORE_750

    def __str__(self):
        return self.vehicle_with_trailer_to_str()

    def vehicle_with_trailer_to_str(self):
        return "{}, trailer({})".format(self.vehicle_to_str(), self._vehicle_trailer)

    def vehicle_to_str_mail(self):
        return f"Type: {self._vehicle_type.lower()}, Merk: {self._vehicle_brand}, Nummerplaat: {self._vehicle_license_plate}, Bouwjaar: {self._vehicle_construction_year}, Chassisnummer: {self._vehicle_chassis_number}, Aanhangwagen: {self._vehicle_trailer}"
