import logging

from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceCoverageOption

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceCoverageOptionSerializerField(ChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceCoverageOption, **kwargs)

    def to_internal_value(self, data):
        # logger.debug("INPUT DATA: %s", data)
        return data

    def to_representation(self, data):
        # logger.debug("OUTPUT DATA: %s", data)
        return data
