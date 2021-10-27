from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import ScoutsGroupContact, ScoutsGroup, GroupAdminLink, GroupAdminAddress
from scouts_auth.serializers import GroupAdminLinkSerializer, GroupAdminAddressSerializer


class ScoutsGroupContactSerializer(serializers.Serializer):

    member: str = serializers.CharField(source="lid")
    oid_member: str = serializers.CharField(source="oidLid")
    function: str = serializers.CharField(source="functie")
    oid_function: str = serializers.CharField(source="oidFunctie")
    name: str = serializers.CharField(source="naam")
    phone: str = serializers.CharField(source="tel", required=False)
    email: str = serializers.CharField(required=False)
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True)

    class Meta:
        model = ScoutsGroupContact
        fields = "__all__"
    
    def get_member(self):
        return self.member if self.member else self.oid_member

    def get_function(self):
        return self.function if self.function else self.oid_function

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
    #contacts: List[ScoutsGroupContact] = ScoutsGroupContactSerializer(source="contacten", many=True)
    contacts: List[ScoutsGroupContact] = None
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True)

    class Meta:
        model = ScoutsGroup
        fields = "__all__"
