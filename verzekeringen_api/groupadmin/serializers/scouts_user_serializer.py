from rest_framework import serializers

from groupadmin.models import ScoutsUser


class ScoutsUserSerializer(serializers.ModelSerializer):

    user_permissions = serializers.SerializerMethodField()
    scouts_groups = serializers.SerializerMethodField()

    class Meta:
        model = ScoutsUser
        fields = "__all__"

    def get_user_permissions(self, obj: ScoutsUser):
        return obj.permissions

    def get_scouts_groups(self, obj: ScoutsUser):
        return [{"group": group.group_admin_id, "name": group.name} for group in obj.scouts_groups]
