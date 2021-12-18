from scouts_insurances.insurances.models.enums import GroupSize

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


class GroupSizeSerializerField(ChoiceSerializerField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=GroupSize, **kwargs)

    def to_representation(self, obj: GroupSize) -> dict:
        data = super().to_representation(obj)
        event_size = GroupSize.from_choice(data)

        return EnumSerializer((event_size[0], event_size[1])).data
