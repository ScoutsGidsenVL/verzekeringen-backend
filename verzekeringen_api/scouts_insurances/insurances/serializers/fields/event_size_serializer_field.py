import logging

from scouts_insurances.insurances.models.enums import EventSize

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


logger = logging.getLogger(__name__)


class EventSizeSerializerField(ChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=EventSize, **kwargs)

    def to_representation(self, obj: EventSize) -> dict:
        data = super().to_representation(obj)
        event_size = EventSize.from_choice(data)

        return EnumSerializer((event_size[0], event_size[1])).data
