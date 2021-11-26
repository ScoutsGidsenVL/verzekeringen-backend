from rest_framework import serializers


class InsuranceCostSerializer(serializers.Serializer):
    total_cost = serializers.DecimalField(max_digits=7, decimal_places=2)
