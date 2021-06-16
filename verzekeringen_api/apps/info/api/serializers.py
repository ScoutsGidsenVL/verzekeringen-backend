from rest_framework import serializers
from ..models import InfoVariable


class InfoVariableOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoVariable
        fields = ("key", "value")
