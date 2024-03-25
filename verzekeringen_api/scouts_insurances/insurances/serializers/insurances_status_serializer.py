import logging

from rest_framework import serializers

from scouts_insurances.insurances.models.enums import InsuranceStatus

logger = logging.getLogger(__name__)


class InsuranceStatusSerializer(serializers.Serializer):

    id = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()
    label = serializers.SerializerMethodField()

    def get_id(self, obj: InsuranceStatus):
        return self.get_value(obj)

    def get_value(self, obj: InsuranceStatus):
        logger.debug("OBJ: %s", obj)
        return obj.value

    def get_label(self, obj: InsuranceStatus):
        return obj.label

    def to_internal_value(self, data: dict) -> dict:
        status = data.pop("status", None)

        return data

    def to_representation(self, data: dict) -> dict:
        # return data.pop("status", None)
        return data
