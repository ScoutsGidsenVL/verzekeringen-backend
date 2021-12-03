from scouts_insurances.insurances.models.enums import GroupSize

from scouts_auth.inuits.serializers.fields import ChoiceSerializerField


class GroupSizeSerializerField(ChoiceSerializerField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, choices=GroupSize, **kwargs)
