from datetime import date

from rest_framework import serializers

from inuits.models import Gender


class ScoutsMemberListSerializer(serializers.Serializer):
    id: str = serializers.CharField(source="group_admin_id")
    last_name: str = serializers.CharField(default="")
    first_name: str = serializers.CharField(default="")
    gender: Gender = serializers.ChoiceField(choices=Gender.choices, default=Gender.UNKNOWN)
    phone_number: str = serializers.CharField(default="")
    email: str = serializers.EmailField(default="")
    birth_date: date = serializers.DateField(default=None)
    group_admin_id: str = serializers.CharField(default="")
