from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicle
from scouts_insurances.equipment.models.enums import TemporaryVehicleInsuranceVehicleTrailerOption
from scouts_insurances.insurances.models import VehicleRelatedInsurance

from scouts_auth.inuits.models.fields import (
    DefaultCharField,
)


class VehicleWithTrailerRelatedInsurance(VehicleRelatedInsurance):

    _vehicle_trailer = DefaultCharField(
        db_column="aanhangwagen",
        choices=TemporaryVehicleInsuranceVehicleTrailerOption.choices,
        max_length=1,
        default=TemporaryVehicleInsuranceVehicle.DEFAULT_VEHICLE_TRAILER_OPTION,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        abstract = True

    # Handle vehicle using seperate class so we can reuse it in other insurances
    @property
    def vehicle(self) -> TemporaryVehicleInsuranceVehicle:
        # If no vehicle type all other fields are empty aswell
        if not self._vehicle_type:
            return None

        return TemporaryVehicleInsuranceVehicle(
            type=self._vehicle_type,
            brand=self._vehicle_brand,
            license_plate=self._vehicle_license_plate,
            construction_year=self._vehicle_construction_year,
            chassis_number=self._vehicle_chassis_number,
            trailer=self._vehicle_trailer,
        )

    @vehicle.setter
    def vehicle(self, obj: TemporaryVehicleInsuranceVehicle = None):
        super().set_vehicle(obj)

        if obj:
            self._vehicle_trailer = obj.trailer

    @property
    def has_trailer(self):
        return self._vehicle_trailer != TemporaryVehicleInsuranceVehicleTrailerOption.NO_TRAILER

    @property
    def has_heavy_trailer(self):
        return self._vehicle_trailer == TemporaryVehicleInsuranceVehicleTrailerOption.TRAILER_MORE_750
