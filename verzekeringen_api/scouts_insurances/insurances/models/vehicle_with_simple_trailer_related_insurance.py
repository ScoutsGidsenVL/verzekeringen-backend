from django.core.validators import MinValueValidator, MaxValueValidator

from scouts_insurances.equipment.models import TravelAssistanceVehicle
from scouts_insurances.equipment.models.enums import TravelAssistanceVehicleTrailerOption
from scouts_insurances.insurances.models import VehicleRelatedInsurance

from scouts_auth.inuits.models.fields import (
    DefaultIntegerField,
)


class VehicleWithSimpleTrailerRelatedInsurance(VehicleRelatedInsurance):

    _vehicle_trailer = DefaultIntegerField(
        db_column="aanhangwagen",
        choices=TravelAssistanceVehicleTrailerOption.choices,
        default=TravelAssistanceVehicle.DEFAULT_VEHICLE_TRAILER_OPTION,
        validators=[MinValueValidator(0), MaxValueValidator(1)],
    )

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Handle vehicle using seperate class so we can reuse it in other insurances
    @property
    def vehicle(self) -> TravelAssistanceVehicle:
        # If no vehicle type all other fields are empty aswell
        if not self._vehicle_type:
            return None

        return TravelAssistanceVehicle(
            type=self._vehicle_type,
            brand=self._vehicle_brand,
            license_plate=self._vehicle_license_plate,
            construction_year=self._vehicle_construction_year,
            trailer=self._vehicle_trailer,
        )

    @vehicle.setter
    def vehicle(self, obj: TravelAssistanceVehicle = None):
        super().set_vehicle(obj)

        if obj:
            self._vehicle_trailer = obj.trailer

    @property
    def has_trailer(self):
        return self._vehicle_trailer != TravelAssistanceVehicleTrailerOption.NO_TRAILER

    @property
    def has_heavy_trailer(self):
        return False
