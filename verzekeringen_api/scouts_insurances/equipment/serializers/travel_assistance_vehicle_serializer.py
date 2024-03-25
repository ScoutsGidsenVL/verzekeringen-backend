from scouts_auth.inuits.serializers.fields import ChoiceSerializerField
from scouts_insurances.equipment.models import TravelAssistanceVehicle
from scouts_insurances.equipment.models.enums import TravelAssistanceVehicleTrailerOption
from scouts_insurances.equipment.serializers import VehicleSerializer


class TravelAssistanceVehicleSerializer(VehicleSerializer):
    trailer = ChoiceSerializerField(
        choices=TravelAssistanceVehicleTrailerOption,
        default=TravelAssistanceVehicle.DEFAULT_VEHICLE_TRAILER_OPTION,
    )

    class Meta:
        model = TravelAssistanceVehicle
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # def validate(self, data: dict) -> TravelAssistanceVehicle:
    #     return TravelAssistanceVehicle(**data)
