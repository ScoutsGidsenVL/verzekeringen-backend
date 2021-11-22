import logging

from django.forms import FileField as DjangoFileField
from django.core.exceptions import ValidationError
from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.insurances.models import EventInsuranceAttachment


logger = logging.getLogger(__name__)


class EventInsuranceAttachmentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    event_insurance = serializers.IntegerField(source="insurance", required=False)

    class Meta:
        model = EventInsuranceAttachment
        fields = ["file", "event_insurance"]

    def validate(self, attrs):
        # There can be only one
        if len(self.initial_data) > 1:
            raise ValidationError("An event insurance can have at most 1 participant list attachment")

        default_error_messages = {
            "invalid_file": "Upload a valid file.",
        }

        for i in self.initial_data.getlist("file"):
            django_field = DjangoFileField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)

        return attrs


class EventInsuranceAttachmentSerializer(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField()
