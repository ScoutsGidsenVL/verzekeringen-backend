from rest_framework import serializers

from scouts_insurances.equipment.models import Equipment
from scouts_insurances.people.serializers import MemberSerializer, NonMemberSerializer


class EquipmentSerializer(serializers.ModelSerializer):
    # id                      pk
    # nature            max_length=50       can be blank
    # description       max_length=500      required
    # total_value       decimal number
    # insurance         references EquipmentInsurance
    # owner_non_member  references NonMember
    # owner_member      references Member

    owner_non_member = NonMemberSerializer(required=False)
    owner_member = MemberSerializer(required=False)

    class Meta:
        model = Equipment
        fields = (
            "id",
            "nature",
            "description",
            "total_value",
            "owner_non_member",
            "owner_member",
        )

    def validate(self, data):
        if data.get("owner_member", None) and data.get("owner_non_member", None):
            raise serializers.ValidationError("There can only be one owner")
        return data
