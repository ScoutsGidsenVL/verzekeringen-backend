import logging

from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOption

# from scouts_auth.inuits.serializers.fields import MultipleChoiceSerializerField
from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceOptionSerializerField(ChoiceSerializerField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceOption, **kwargs)

    def to_internal_value(self, data):
        if isinstance(data, list):
            data = int("".join([str(sub_value) for sub_value in data]))

        return super().to_internal_value(data)
