import logging

from rest_framework import serializers

from scouts_auth.models import GroupAdminAddress


logger = logging.getLogger(__name__)


class GroupAdminAddressSerializer(serializers.Serializer):

    street: str = serializers.CharField(source="straat")
    number: str = serializers.CharField(source="nummer")
    letter_box: str = None
    postcode_city = None
    postal_code: str = serializers.CharField(source="postcode")
    city: str = serializers.CharField(source="gemeente")
    country: str = serializers.CharField(source="land")
    phone: str = serializers.CharField(source="telefoon")
    postal_address: bool = serializers.BooleanField(source="postadres")
    status: str = serializers.CharField()
    position: dict = None
    giscode: str = serializers.CharField()
    description: str = serializers.CharField(source="omschrijving")

    class Meta:
        model = GroupAdminAddress
        fields = "__all__"
