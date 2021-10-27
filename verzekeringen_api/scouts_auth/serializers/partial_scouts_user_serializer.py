from rest_framework import serializers

from scouts_auth.models import PartialScoutsUser

class PartialScoutsUserSerializer(serializers.Serializer):
    
    class Meta:
        model = PartialScoutsUser
        fields = "__all__"
