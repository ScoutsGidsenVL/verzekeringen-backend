from rest_framework import serializers

from scouts_insurances.insurances.models import InsuranceType


class InsuranceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceType
        fields = ("id", "name", "description", "max_term")
