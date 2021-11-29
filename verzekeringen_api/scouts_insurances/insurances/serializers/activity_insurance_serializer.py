from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from scouts_auth.inuits.filters.helpers import parse_choice_to_tuple
from scouts_auth.inuits.serializers import EnumSerializer

from scouts_insurances.insurances.models import ActivityInsurance
from scouts_insurances.insurances.models.enums import GroupSize
from apps.insurances.models import ActivityInsuranceAttachment
from apps.insurances.serializers import ActivityInsuranceAttachmentSerializer
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer


class ActivityInsuranceSerializer(BaseInsuranceSerializer):

    group_size = serializers.SerializerMethodField()
    participant_list_file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = ActivityInsurance
        fields = BaseInsuranceFields + ("nature", "group_size", "postal_code", "city", "participant_list_file")

    @swagger_serializer_method(serializer_or_field=EnumSerializer)
    def get_group_size(self, obj):
        return EnumSerializer(parse_choice_to_tuple(GroupSize(obj.group_size))).data

    @swagger_serializer_method(serializer_or_field=ActivityInsuranceAttachmentSerializer)
    def get_participant_list_file(self, obj: ActivityInsurance):
        try:
            attachment: ActivityInsuranceAttachment = obj.attachment

            if attachment:
                return ActivityInsuranceAttachmentSerializer(attachment, context=self.context).data
        except Exception:
            return None
