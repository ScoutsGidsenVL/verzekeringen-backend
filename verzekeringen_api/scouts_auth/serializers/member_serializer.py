from typing import List
from datetime import date

from rest_framework import serializers

from scouts_auth.models import GroupAdminMember, Gender, GroupAdminAddress, GroupAdminContact, ScoutsFunction
from scouts_auth.serializers import GroupAdminAddressSerializer, GroupAdminContactSerializer, ScoutsFunctionSerializer


class PersonalDataSerializer(serializers.Serializer):

    gender: Gender = serializers.SerializerMethodField()
    phone: str = serializers.CharField(source="gsm", required="")

    def get_gender(self, obj):
        return obj.get_gender()





class GroupAdminMemberSerializer(serializers.Serializer):

    first_name: str = serializers.CharField(source="voornaam", required=False)
    last_name: str = serializers.CharField(source="achternaam", required=False)
    # gender: Gender = None
    # phone_number: str = serializers.CharField(source="gsm", required=False)
    personal_data = PersonalDataSerializer(source="persoonsgegevens", required=False)
    birth_date: date = serializers.DateField(required=False)
    email: str = serializers.CharField(required=False)
    group_admin_id:str = serializers.CharField(source="id", required=False)
    membership_number: str = serializers.CharField(required=False)
    username: str = serializers.CharField(source="gebruikersnaam", required=False)
    addresses: List[GroupAdminAddress] = GroupAdminAddressSerializer(source="addressen", required=False, many=True)
    contacts: List[GroupAdminContact] = GroupAdminContactSerializer(source="contacten", required=False, many=True)
    functions: List[ScoutsFunction] = ScoutsFunctionSerializer(source="functies", required=False, many=True)

    class Meta:
        model = GroupAdminMember
        fields = "__all__"
        depth = 1
    
    def create(self, validated_data):
        self.username = validated_data.pop("gebruikersnaam", "")

