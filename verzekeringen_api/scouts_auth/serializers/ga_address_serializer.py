import logging

from rest_framework import serializers

from scouts_auth.models import GroupAdminAddress


logger = logging.getLogger(__name__)


class GroupAdminAddressSerializer(serializers.Serializer):

    id: str = serializers.CharField(required=False)
    street: str = serializers.CharField(source="straat", required=False)
    number: str = serializers.CharField(source="nummer", required=False)
    letter_box: str = serializers.CharField(source="bus", required=False)
    postcode_city = None
    postal_code: str = serializers.CharField(source="postcode", required=False)
    city: str = serializers.CharField(source="gemeente", required=False)
    country: str = serializers.CharField(source="land", required=False)
    phone: str = serializers.CharField(source="telefoon", required=False)
    postal_address: bool = serializers.BooleanField(source="postadres", default=False)
    status: str = serializers.CharField(required=False)
    position: dict = None
    giscode: str = serializers.CharField(required=False)
    description: str = serializers.CharField(source="omschrijving", required=False)

    class Meta:
        model = GroupAdminAddress
        fields = "__all__"
