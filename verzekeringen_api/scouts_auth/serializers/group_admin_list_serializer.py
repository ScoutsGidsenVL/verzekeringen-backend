from rest_framework import serializers

from scouts_auth.models import Gender


class GroupAdminMemberListSerializer(serializers.Serializer):
    id = serializers.CharField(source="group_admin_id")
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    gender = serializers.ChoiceField(choices=Gender.choices)
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    birth_date = serializers.DateField()
    group_admin_id = serializers.CharField()
