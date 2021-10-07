from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.insurances.models import InsuranceClaim, InsuranceClaimAttachment


class InsuranceClaimAttachmentUploadSerializer(serializers.Serializer):
    insurance_claim = serializers.PrimaryKeyRelatedField(queryset=InsuranceClaim.objects.all())
    file = serializers.FileField(required=False)


class InsuranceClaimAttachmentSerializer(serializers.Serializer):
    id = serializers.CharField()
    url = serializers.CharField()


class FileDetailOutputSerializer(serializers.ModelSerializer):

    name = serializers.SerializerMethodField()
    size = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceClaimAttachment
        fields = (
            "id",
            "content_type",
            "name",
            "size",
        )

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_name(self, InsuranceClaimAttachment):
        if InsuranceClaimAttachment.file.name:
            return InsuranceClaimAttachment.file.name
        else:
            return None

    @swagger_serializer_method(serializer_or_field=serializers.CharField)
    def get_size(self, InsuranceClaimAttachment):
        if InsuranceClaimAttachment.file.size:
            return InsuranceClaimAttachment.file.size
        else:
            return None
