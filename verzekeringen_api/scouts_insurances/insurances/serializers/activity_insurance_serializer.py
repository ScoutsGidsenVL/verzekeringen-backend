import logging

from django.core.exceptions import ValidationError
from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method


from scouts_insurances.insurances.models import ActivityInsurance
from apps.insurances.models import ActivityInsuranceAttachment
from apps.insurances.serializers import ActivityInsuranceAttachmentSerializer
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import GroupSizeSerializerField


logger = logging.getLogger(__name__)


class ActivityInsuranceSerializer(BaseInsuranceSerializer):

    group_size = GroupSizeSerializerField()
    participant_list_file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = ActivityInsurance
        fields = BaseInsuranceFields + ["nature", "group_size", "postal_code", "city", "participant_list_file"]

    @swagger_serializer_method(serializer_or_field=ActivityInsuranceAttachmentSerializer)
    def get_participant_list_file(self, obj: ActivityInsurance):
        try:
            attachment: ActivityInsuranceAttachment = obj.attachment

            if attachment:
                return ActivityInsuranceAttachmentSerializer(attachment, context=self.context).data
        except Exception:
            return None

    def validate(self, data: dict) -> dict:
        logger.debug("SERIALIZER VALIDATE DATA: %s", data)
        group_size = data.get("group_size", None)

        if not group_size:
            raise ValidationError("Group size must be given")

        return super().validate(data)
