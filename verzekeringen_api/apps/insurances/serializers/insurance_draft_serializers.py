from rest_framework import serializers

from apps.insurances.models import InsuranceDraft

from scouts_insurances.insurances.serializers import InsuranceTypeSerializer


class InsuranceDraftSerializer(serializers.ModelSerializer):
    insurance_type = InsuranceTypeSerializer()
    data = serializers.JSONField()

    class Meta:
        model = InsuranceDraft
        fields = ("id", "created_on", "insurance_type", "data")
