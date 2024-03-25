import logging

# from scouts_auth.inuits.serializers.fields import MultipleChoiceSerializerField
from scouts_auth.inuits.serializers.fields import ChoiceSerializerField
from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOption

logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceOptionSerializerField(ChoiceSerializerField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceOption, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, list):
            data = int("".join([str(sub_value) for sub_value in data if sub_value]))

        return super().to_internal_value(data)
