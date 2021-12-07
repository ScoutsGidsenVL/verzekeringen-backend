import logging

from django.core.exceptions import ValidationError

from scouts_insurances.insurances.models import EventInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import EventSizeSerializerField


logger = logging.getLogger(__name__)


class EventInsuranceSerializer(BaseInsuranceSerializer):

    event_size = EventSizeSerializerField()

    class Meta:
        model = EventInsurance
        fields = BaseInsuranceFields + ["nature", "event_size", "postal_code", "city"]

    def validate(self, data: dict) -> dict:
        logger.debug("SERIALIZER VALIDATE DATA: %s", data)
        event_size = data.get("event_size", None)

        if not event_size:
            raise ValidationError("Event size must be given")

        return super().validate(data)
