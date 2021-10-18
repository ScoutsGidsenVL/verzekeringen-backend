from rest_framework import serializers

from apps.info.models import InfoVariable


class InfoVariableOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InfoVariable
        fields = ("key", "value")
