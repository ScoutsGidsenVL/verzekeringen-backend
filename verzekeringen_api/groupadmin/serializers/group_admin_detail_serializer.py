from rest_framework import serializers

from groupadmin.serializers import (
    ScoutsMemberListSerializer,
    BelgianPostcodeCitySerializer,
)


class ScoutsMemberDetailSerializer(ScoutsMemberListSerializer):

    id: str = serializers.CharField(default="")
    membership_number = serializers.IntegerField(default=0)
    street = serializers.CharField(source="address.street", default="")
    number = serializers.CharField(source="address.number", default="")
    letter_box = serializers.CharField(source="address.letter_box", default="")
    postcode_city = BelgianPostcodeCitySerializer(source="address.postcode_city", default="")
