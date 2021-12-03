from scouts_insurances.insurances.models.enums import EventSize

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


class EventSizeSerializerField(ChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=EventSize, **kwargs)
