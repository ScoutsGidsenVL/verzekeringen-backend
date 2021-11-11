from rest_framework import serializers

from groupadmin.models import ScoutsUser
from groupadmin.serializers import ScoutsMemberSerializer


class ScoutsUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoutsUser
        fields = "__all__"
