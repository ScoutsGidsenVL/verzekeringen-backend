from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import GroupAdminContact, ScoutsGroup, GroupAdminLink, GroupAdminAddress
from scouts_auth.serializers import GroupAdminLinkSerializer, GroupAdminAddressSerializer


class ScoutsGroupSerializer(serializers.Serializer):
    """Serializes a Group instance to a string."""

    id: str = serializers.CharField(required=False)
    number: str = serializers.CharField(source="groepsnummer", required=False)
    name: str = serializers.CharField(source="naam", required=False)
    addresses: List[GroupAdminAddress] = GroupAdminAddressSerializer(source="addressen", required=False, many=True)
    date_of_foundation: date = serializers.DateTimeField(source="opgericht", required=False)
    bank_account: str = serializers.CharField(source="rekeningnummer", required=False)
    email: str = serializers.CharField(required=False)
    website: str = serializers.CharField(required=False)
    info: str = serializers.CharField(source="vrijeInfo", required=False)
    #contacts: List[ScoutsGroupContact] = ScoutsGroupContactSerializer(source="contacten", many=True)
    contacts: List[GroupAdminContact] = None
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, required=False)

    class Meta:
        model = ScoutsGroup
        fields = "__all__"
