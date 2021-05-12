from rest_framework import serializers
from ..models import User


class UserDetailOutputSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "date_joined", "permissions")

    def get_permissions(self, obj):
        return obj.get_all_permissions()


class UserNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "date_joined")
