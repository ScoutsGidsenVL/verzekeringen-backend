from rest_framework import serializers

from scouts_auth.models import ScoutsFunction

class ScoutsFunctionSerializer(serializers.Serializer):

    class Meta:
        model = ScoutsFunction
        fields = "__all__"
