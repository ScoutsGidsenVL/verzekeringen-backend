from rest_framework import serializers

from scouts_auth.models import User
from scouts_auth.serializers import ScoutsGroupSerializer


class UserSerializer(serializers.ModelSerializer):
    """
    Serializes a User instance into a string.
    """

    permissions = serializers.SerializerMethodField()
    birth_date = serializers.DateField()
    membership_number = serializers.CharField()
    phone_number = serializers.CharField()
    scouts_groups = ScoutsGroupSerializer(many=True)

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
            "group_admin_id",
        )

    def get_permissions(self, obj):
        return obj.get_all_permissions()


# COMMENTED out because it doesn't appear to be used anywhere
# class UserNestedOutputSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = User
#        fields = ('id', 'first_name', 'last_name', 'email', 'date_joined')
