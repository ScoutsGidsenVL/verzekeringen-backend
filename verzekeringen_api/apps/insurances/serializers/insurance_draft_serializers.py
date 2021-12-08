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
        insurance_type_serializer = InsuranceTypeSerializer(
            data=InsuranceType.objects.get(pk=data.get("insurance_type"))
        )
        insurance_type_serializer.is_valid(raise_exception=True)

        data["insurance_type"] = insurance_type_serializer.validated_data

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: InsuranceDraft) -> dict:
        data = super().to_representation(obj)

        data["insurance_type"] = data.pop("insurance_type").get("id")

        return data
