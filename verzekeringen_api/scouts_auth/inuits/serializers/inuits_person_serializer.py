from rest_framework import serializers

from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.serializers import InuitsAddressSerializer, InuitsPersonalDetailsSerializer


class InuitsPersonSerializer(InuitsPersonalDetailsSerializer, InuitsAddressSerializer, serializers.ModelSerializer):
    class Meta:
        model = InuitsPerson
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
