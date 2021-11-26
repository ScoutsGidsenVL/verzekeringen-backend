from rest_framework import serializers

from scouts_insurances.info.models import InfoVariable


class InfoVariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoVariable
        fields = ("key", "value")
