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
        serializer = InsuranceTypeSerializer(data=InsuranceType.objects.get(pk=int(data.get("insurance_type"))))
        serializer.is_valid(raise_exception=False)

        data["insurance_type"] = serializer.validated_data
        data = super().to_internal_value(data)

        return data
