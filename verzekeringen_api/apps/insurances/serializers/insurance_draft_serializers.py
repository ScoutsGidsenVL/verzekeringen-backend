from rest_framework import serializers

from apps.insurances.models import InsuranceDraft

from scouts_insurances.insurances.models import InsuranceType
from scouts_insurances.insurances.serializers import InsuranceTypeSerializer


class InsuranceDraftSerializer(serializers.ModelSerializer):
    insurance_type = InsuranceTypeSerializer()
    data = serializers.JSONField()

    class Meta:
        model = InsuranceDraft
        fields = "__all__"

    def to_internal_value(self, data: dict) -> dict:

        data = super().to_internal_value(data)
        data["insurance_type"] = InsuranceTypeSerializer(InsuranceType.objects.get(id=data.get("insurance_type"))).data

        return data
