from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceCoverageOption

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


class TemporaryVehicleInsuranceCoverageOptionSerializerField(ChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceCoverageOption, **kwargs)
