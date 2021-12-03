from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOption

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


class TemporaryVehicleInsuranceOptionSerializerField(ChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceOption, **kwargs)
