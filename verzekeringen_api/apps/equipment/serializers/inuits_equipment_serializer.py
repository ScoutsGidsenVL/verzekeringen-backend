import logging

from rest_framework import serializers

from apps.equipment.models import InuitsEquipment
from apps.people.serializers.fields import InuitsNonMemberSerializerField

from scouts_auth.groupadmin.models import AbstractScoutsMember, AbstractScoutsGroup
from scouts_auth.groupadmin.serializers.fields import (
    AbstractScoutsMemberSerializerField,
    AbstractScoutsGroupSerializerField,
)


logger = logging.getLogger(__name__)


class InuitsEquipmentSerializer(serializers.ModelSerializer):

    # id                            pk
    # nature                        max_length=50                   is optional
    # description                   max_length=500                  is optional
    # total_value                   decimal field
    # owner_non_member              references InuitsNonMember
    # owner_member_group_admin_id   group admin id of owner member
    # owner_group_group_admin_id    group admin id of owner group

    # owner_non_member = InuitsEquipmentNonMemberRelatedField(required=False, allow_null=True)
    owner_non_member = InuitsNonMemberSerializerField(required=False, allow_null=True)
    # owner_non_member = serializers.SerializerMethodField()
    owner_member = AbstractScoutsMemberSerializerField(required=False, allow_null=True)
    owner_group = AbstractScoutsGroupSerializerField(required=False, allow_null=True)

    class Meta:
        model = InuitsEquipment
        fields = (
            "id",
            "nature",
            "description",
            "total_value",
            "owner_non_member",
            "owner_member",
            "owner_group",
        )

    def validate(self, data):
        owner_non_member = data.get("owner_non_member", None)
        owner_member = data.get("owner_member", None)
        owner_group = data.get("owner_group", None)

        if not owner_member and not owner_non_member and not owner_group:
            raise serializers.ValidationError("A piece of equipment needs an owner")
        if owner_member and owner_non_member and owner_group:
            raise serializers.ValidationError("There can only be one owner of the piece of equipment")
        if owner_group and (owner_member or owner_non_member):
            logger.warn(
                "A piece of equipment either belongs to a person or to a scouts group - Removing group as owner"
            )
            data["owner_group"] = None

        if owner_member and not isinstance(owner_member, AbstractScoutsMember):
            raise serializers.ValidationError(
                "AbstractScoutsMember instance couldn't be loaded with the provided group admin id"
            )

        if owner_group and not isinstance(owner_group, AbstractScoutsGroup):
            raise serializers.ValidationError(
                "AbstractScoutsGroup instance couldn't be loaded with the provided group admin id"
            )

        return data
