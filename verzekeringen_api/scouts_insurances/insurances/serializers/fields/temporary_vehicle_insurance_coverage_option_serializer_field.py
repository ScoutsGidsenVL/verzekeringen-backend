import logging

from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceCoverageOption

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceCoverageOptionSerializerField(ChoiceSerializerField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceCoverageOption, **kwargs)
