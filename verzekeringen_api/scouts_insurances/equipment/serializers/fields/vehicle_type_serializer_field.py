import logging

from scouts_insurances.equipment.models.enums import VehicleType

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


logger = logging.getLogger(__name__)


class VehicleTypeSerializerField(ChoiceSerializerField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=VehicleType, **kwargs)
