from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOption

from scouts_auth.inuits.serializers.fields import MultipleChoiceSerializerField


class TemporaryVehicleInsuranceOptionSerializerField(MultipleChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceOption, **kwargs)
