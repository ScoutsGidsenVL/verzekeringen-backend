from rest_framework import serializers

from apps.insurances.models import InsuranceType


# Output
class InsuranceTypeOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = ("id", "name", "description", "max_term")
