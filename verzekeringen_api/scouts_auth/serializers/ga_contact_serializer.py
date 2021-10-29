from typing import List

from rest_framework import serializers

from scouts_auth.models import GroupAdminContact, GroupAdminLink
from scouts_auth.serializers import GroupAdminLinkSerializer

class GroupAdminContactSerializer(serializers.Serializer):
    
    member: str = serializers.CharField(source="lid", required=False)
    oid_member: str = serializers.CharField(source="oidLid", required=False)
    function: str = serializers.CharField(source="functie", required=False)
    oid_function: str = serializers.CharField(source="oidFunctie", required=False)
    name: str = serializers.CharField(source="naam", required=False)
    phone: str = serializers.CharField(source="tel", required=False)
    email: str = serializers.CharField(required=False)
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True)

    class Meta:
        model = GroupAdminContact
        fields = "__all__"
    
    def get_member(self):
        return self.member if self.member else self.oid_member

    def get_function(self):
        return self.function if self.function else self.oid_function