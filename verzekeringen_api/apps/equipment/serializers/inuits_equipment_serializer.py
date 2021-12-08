import logging

from rest_framework import serializers

from apps.equipment.models import InuitsEquipment
from apps.people.models import InuitsNonMember
from apps.people.serializers import InuitsNonMemberSerializer

from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer, AbstractScoutsGroupSerializer
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.serializers.fields import OptionalCharField


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
    owner_non_member = InuitsNonMemberSerializer(required=False, allow_null=True)
    # owner_non_member = serializers.SerializerMethodField()
    owner_member = AbstractScoutsMemberSerializer(required=False, allow_null=True)
    owner_group = AbstractScoutsGroupSerializer(required=False, allow_null=True)

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

    def to_internal_value(self, data: dict) -> dict:
        owner_non_member = data.pop("owner_non_member", None)
        if owner_non_member:
            data["owner_non_member"] = InuitsNonMember.objects.get(id=owner_non_member)
        else:
            data["owner_non_member"] = None

        owner_member = data.pop("owner_member", None)
        if owner_member:
            data["owner_member"] = GroupAdmin().get_member_info(
                active_user=self.context.get("request").user, group_admin_id=owner_member
            )
        else:
            data["owner_member"] = None

        owner_group = data.pop("owner_group", None)
        if owner_group:
            data["owner_group"] = GroupAdmin().get_group(
                active_user=self.context.get("request").user, group_group_admin_id=owner_group
            )
        else:
            data["owner_group"] = None

        return data

    def validate(self, data):
        logger.debug("SERIALIZER VALIDATE DATA: %s", data)

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
        return data
