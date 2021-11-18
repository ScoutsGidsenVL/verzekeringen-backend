from rest_framework import serializers

from groupadmin.models import ScoutsUser


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        fields = "__all__"

    def get_user_permissions(self, obj: ScoutsUser):
        return obj.permissions
