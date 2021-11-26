import logging

from django.forms import FileField as DjangoFileField
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.insurances.models import ActivityInsuranceAttachment


logger = logging.getLogger(__name__)


class ActivityInsuranceAttachmentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)
    insurance = serializers.IntegerField(required=False)

    class Meta:
        model = ActivityInsuranceAttachment
        fields = ["file", "insurance"]

    def validate(self, attrs):
        # There can be only one
        if len(self.initial_data.getlist("file")) > 1:
            raise ValidationError("An insurance can have at most 1 participant list attachment")

        default_error_messages = {
            "invalid_file": "Upload a valid file.",
        }

        for i in self.initial_data.getlist("file"):
            django_field = DjangoFileField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)

        return attrs


class ActivityInsuranceAttachmentSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    filename = serializers.SerializerMethodField()

    class Meta:
        model = ActivityInsuranceAttachment
        exclude = ("insurance", "file")

    def get_id(self, obj: ActivityInsuranceAttachment):
        return obj.id

    def get_url(self, obj: ActivityInsuranceAttachment):
        return self.context.get("request").build_absolute_uri(
            "/api/activities/participants/" + str(obj.id) + "/download"
        )

    def get_filename(self, obj: ActivityInsuranceAttachment):
        return obj.file.name
