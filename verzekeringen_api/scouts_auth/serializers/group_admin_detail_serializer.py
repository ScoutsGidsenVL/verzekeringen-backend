from rest_framework import serializers

from scouts_auth.serializers import (
    GroupAdminMemberListSerializer,
    BelgianPostcodeCitySerializer,
)


class GroupAdminMemberDetailSerializer(GroupAdminMemberListSerializer):

    id: str = serializers.CharField(default="")
    membership_number = serializers.IntegerField(default=0)
    street = serializers.CharField(source="address.street", default="")
    number = serializers.CharField(source="address.number", default="")
    letter_box = serializers.CharField(source="address.letter_box", default="")
    postcode_city = BelgianPostcodeCitySerializer(source="address.postcode_city", default="")
