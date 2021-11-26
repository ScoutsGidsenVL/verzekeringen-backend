import logging

from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.insurances.models import EventInsuranceAttachment
from apps.insurances.serializers import EventInsuranceAttachmentSerializer

from scouts_insurances.insurances.models import EventInsurance
from scouts_insurances.insurances.models.enums import EventSize
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer

from inuits.serializers import EnumSerializer
from inuits.filters.helpers import parse_choice_to_tuple


logger = logging.getLogger(__name__)


class EventInsuranceSerializer(BaseInsuranceSerializer):

    event_size = serializers.SerializerMethodField()
    participant_list_file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = EventInsurance
        fields = BaseInsuranceFields + ("nature", "event_size", "postal_code", "city", "participant_list_file")

    @swagger_serializer_method(serializer_or_field=EnumSerializer)
    def get_event_size(self, obj):
        return EnumSerializer(parse_choice_to_tuple(EventSize(obj.event_size))).data

    @swagger_serializer_method(serializer_or_field=EventInsuranceAttachmentSerializer)
    def get_participant_list_file(self, obj: EventInsurance):
        try:
            attachment: EventInsuranceAttachment = obj.attachment

            if attachment:
                return EventInsuranceAttachmentSerializer(attachment, context=self.context).data
        except Exception:
            return None
