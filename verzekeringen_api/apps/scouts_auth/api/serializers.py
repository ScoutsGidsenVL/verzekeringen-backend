from rest_framework import serializers
from ..models import User


class GroupOutputSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    location = serializers.CharField()


class UserDetailOutputSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()
    birth_date = serializers.DateField()
    membership_number = serializers.CharField()
    phone_number = serializers.CharField()
    scouts_groups = GroupOutputSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "birth_date",
            "membership_number",
            "phone_number",
            "scouts_groups",
            "date_joined",
            "permissions",
        )

    def get_permissions(self, obj):
        return obj.get_all_permissions()


class UserNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "email", "date_joined")
