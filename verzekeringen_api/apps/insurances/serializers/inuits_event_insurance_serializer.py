import logging

from django.core.exceptions import ValidationError
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from apps.insurances.models import EventInsuranceAttachment
from apps.insurances.serializers import EventInsuranceAttachmentSerializer
from scouts_insurances.insurances.models import EventInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, EventInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import EventSizeSerializerField

logger = logging.getLogger(__name__)


class InuitsEventInsuranceSerializer(EventInsuranceSerializer):

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
