from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from django.conf import settings
from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from ...models import InsuranceDraft, InsuranceType
from .insurance_type_serializers import InsuranceTypeOutputSerializer


class InsuranceDraftOutputSerializer(serializers.ModelSerializer):
    insurance_type = InsuranceTypeOutputSerializer()

    class Meta:
        model = InsuranceDraft
        fields = ("id", "created_on", "insurance_type", "data")


class InsuranceDraftCreateInputSerializer(serializers.Serializer):
    insurance_type = serializers.PrimaryKeyRelatedField(queryset=InsuranceType.objects.all())
    data = serializers.JSONField()
