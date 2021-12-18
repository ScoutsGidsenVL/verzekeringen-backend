import logging

from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicle
from scouts_insurances.equipment.models.enums import TemporaryVehicleInsuranceVehicleTrailerOption
from scouts_insurances.equipment.serializers import VehicleSerializer

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceVehicleSerializer(VehicleSerializer):
    trailer = ChoiceSerializerField(
        choices=TemporaryVehicleInsuranceVehicleTrailerOption,
        default=TemporaryVehicleInsuranceVehicle.DEFAULT_VEHICLE_TRAILER_OPTION,
    )

    class Meta:
        model = TemporaryVehicleInsuranceVehicle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate(self, data: dict) -> TemporaryVehicleInsuranceVehicle:
        return TemporaryVehicleInsuranceVehicle(**data)
