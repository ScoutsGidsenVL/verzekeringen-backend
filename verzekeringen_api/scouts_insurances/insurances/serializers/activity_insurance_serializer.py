import logging

from django.core.exceptions import ValidationError

from scouts_insurances.insurances.models import ActivityInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import GroupSizeSerializerField

logger = logging.getLogger(__name__)


class ActivityInsuranceSerializer(BaseInsuranceSerializer):

    group_size = GroupSizeSerializerField()

    class Meta:
        model = ActivityInsurance
        fields = BaseInsuranceFields + ["nature", "group_size", "postal_code", "city"]

    def validate(self, data: dict) -> dict:
        logger.debug("SERIALIZER VALIDATE DATA: %s", data)
        group_size = data.get("group_size", None)

        if not group_size:
            raise ValidationError("Group size must be given")

        return super().validate(data)
