import logging

from rest_framework import serializers


logger = logging.getLogger(__name__)


class MultipleChoiceSerializerField(serializers.MultipleChoiceField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def bind(self, field_name, parent):
        # logger.debug("FIELD NAME: %s", field_name)
        return super().bind(field_name, parent)

    def get_value(self, dictionary):
        # logger.debug("DICT: %s", dictionary)
        value = super().get_value(dictionary)
        return value

    def to_internal_value(self, data):
        # logger.debug("DATA: %s", data)
        return super().to_internal_value(data)

    def to_representation(self, value):
        # logger.debug("REPR: %s", value)
        return super().to_representation(value)

    def validate(self, value):
        # logger.debug("CHOICE VALIDATE VALUE: %s", value)
        return super().validate(value)