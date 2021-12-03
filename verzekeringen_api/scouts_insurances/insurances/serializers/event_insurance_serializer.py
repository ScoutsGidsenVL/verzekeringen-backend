import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.insurances.models import EventInsuranceAttachment
from apps.insurances.serializers import EventInsuranceAttachmentSerializer

from scouts_insurances.insurances.models import EventInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import EventSizeSerializerField


logger = logging.getLogger(__name__)


class EventInsuranceSerializer(BaseInsuranceSerializer):

    event_size = EventSizeSerializerField()
    participant_list_file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = EventInsurance
        fields = BaseInsuranceFields + ["nature", "event_size", "postal_code", "city", "participant_list_file"]

    @swagger_serializer_method(serializer_or_field=EventInsuranceAttachmentSerializer)
    def get_participant_list_file(self, obj: EventInsurance):
        try:
            attachment: EventInsuranceAttachment = obj.attachment

            if attachment:
                return EventInsuranceAttachmentSerializer(attachment, context=self.context).data
        except Exception:
            return None

    def validate(self, data: dict) -> dict:
        logger.debug("SERIALIZER VALIDATE DATA: %s", data)
        event_size = data.get("event_size", None)

        if not event_size:
            raise ValidationError("Event size must be given")

        return super().validate(data)
