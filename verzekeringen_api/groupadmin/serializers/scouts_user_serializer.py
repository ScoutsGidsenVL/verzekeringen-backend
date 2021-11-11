from rest_framework import serializers

from groupadmin.models import ScoutsUser


class ScoutsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutsUser
        fields = "__all__"
