from rest_framework import serializers
from apps.insurances.models import InsuranceDraft, InsuranceType
from . import InsuranceTypeOutputSerializer


class InsuranceDraftOutputSerializer(serializers.ModelSerializer):
    insurance_type = InsuranceTypeOutputSerializer()

    class Meta:
        model = InsuranceDraft
        fields = ("id", "created_on", "insurance_type", "data")


class InsuranceDraftCreateInputSerializer(serializers.Serializer):
    insurance_type = serializers.PrimaryKeyRelatedField(queryset=InsuranceType.objects.all())
    data = serializers.JSONField()
