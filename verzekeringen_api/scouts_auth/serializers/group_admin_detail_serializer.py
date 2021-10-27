from rest_framework import serializers

from scouts_auth.serializers import (
    GroupAdminMemberListSerializer,
    BelgianPostcodeCitySerializer,
)


class GroupAdminMemberDetailSerializer(GroupAdminMemberListSerializer):
    membership_number = serializers.IntegerField()
    street = serializers.CharField(source="address.street")
    number = serializers.CharField(source="address.number")
    letter_box = serializers.CharField(source="address.letter_box")
    postcode_city = BelgianPostcodeCitySerializer(source="address.postcode_city")
