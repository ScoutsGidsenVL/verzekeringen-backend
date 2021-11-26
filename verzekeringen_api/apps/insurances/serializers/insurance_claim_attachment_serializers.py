import logging

from django.forms import FileField as DjangoFileField
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.insurances.models import InsuranceClaimAttachment


logger = logging.getLogger(__name__)


class InsuranceClaimAttachmentUploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=False)

    class Meta:
        model = InsuranceClaimAttachment
        fields = ["file", "insurance_claim"]
        extra_kwargs = {"insurance_claim": {"required": False}}

    def validate(self, attrs):
        # There can be only one
        if len(self.initial_data) > 1:
            raise ValidationError("An insurance claim can have at most 1 attachment")

        default_error_messages = {
            "invalid_file": "Upload a valid file.",
        }

        for i in self.initial_data.getlist("file"):
            django_field = DjangoFileField()
            django_field.error_messages = default_error_messages
            django_field.clean(i)

        return attrs


class InsuranceClaimAttachmentSerializer(serializers.Serializer):
    filename = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceClaimAttachment
        exclude = ("insurance_claim", "file")

    def get_filename(self, obj: InsuranceClaimAttachment):
        return obj.file.name


# class FileDetailOutputSerializer(serializers.ModelSerializer):

#     name = serializers.SerializerMethodField()
#     size = serializers.SerializerMethodField()

#     class Meta:
#         model = InsuranceClaimAttachment
#         fields = (
#             "id",
#             "content_type",
#             "name",
#             "size",
#         )

#     @swagger_serializer_method(serializer_or_field=serializers.CharField)
#     def get_name(self, InsuranceClaimAttachment):
#         if InsuranceClaimAttachment.file.name:
#             return InsuranceClaimAttachment.file.name
#         else:
#             return None

#     @swagger_serializer_method(serializer_or_field=serializers.CharField)
#     def get_size(self, InsuranceClaimAttachment):
#         if InsuranceClaimAttachment.file.size:
#             return InsuranceClaimAttachment.file.size
#         else:
#             return None
