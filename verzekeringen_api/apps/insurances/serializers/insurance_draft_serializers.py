from rest_framework import serializers

from apps.insurances.models import InsuranceDraft

from scouts_insurances.insurances.models import InsuranceType


class InsuranceDraftSerializer(serializers.ModelSerializer):
    insurance_type = serializers.PrimaryKeyRelatedField(queryset=InsuranceType.objects.all())
    data = serializers.JSONField()

    class Meta:
        model = InsuranceDraft
        fields = "__all__"
