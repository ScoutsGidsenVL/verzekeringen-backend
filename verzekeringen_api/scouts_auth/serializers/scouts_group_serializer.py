from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import ScoutsGroupContact, ScoutsGroup, GroupAdminLink, GroupAdminAddress
from . import GroupAdminLinkSerializer, GroupAdminAddressSerializer


class ScoutsGroupContactSerializer(serializers.Serializer):

    member: str = serializers.CharField(source="lid")
    function: str = serializers.CharField(source="functie")
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True)

    class Meta:
        model = ScoutsGroupContact
        fields = "__all__"


class ScoutsGroupSerializer(serializers.Serializer):
    """Serializes a Group instance to a string."""

    id: str = serializers.CharField()
    number: str = serializers.CharField(source="groepsnummer")
    name: str = serializers.CharField(source="naam")
    addresses: List[GroupAdminAddress] = GroupAdminAddressSerializer(source="addressen", many=True)
    date_of_foundation: date = serializers.DateTimeField(source="opgericht")
    bank_account: str = serializers.CharField(source="rekeningnummer")
    email: str = serializers.CharField()
    website: str = serializers.CharField()
    info: str = serializers.CharField(source="vrijeInfo")
    contacts: List[ScoutsGroupContact] = ScoutsGroupContactSerializer(source="contacten", many=True)
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True)

    class Meta:
        model = ScoutsGroup
        fields = "__all__"
