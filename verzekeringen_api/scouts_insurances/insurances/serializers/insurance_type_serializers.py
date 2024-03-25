import logging

from rest_framework import serializers

from scouts_insurances.insurances.models import InsuranceType

logger = logging.getLogger(__name__)


class InsuranceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = "__all__"

    def to_internal_value(self, data):
        logger.debug("INSURANCE TYPE SERIALIZER: %s", data)
        return data
