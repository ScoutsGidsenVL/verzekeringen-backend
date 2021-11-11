from rest_framework import serializers

from groupadmin.models import ScoutsUser


class ScoutsUserSerializer(serializers.Serializer):
    class Meta:
        model = ScoutsUser
        fields = "__all__"
