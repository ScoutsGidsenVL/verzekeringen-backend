import logging

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField
from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceCoverageOption

logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceCoverageOptionSerializerField(ChoiceSerializerField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=TemporaryVehicleInsuranceCoverageOption, **kwargs)
