import logging

from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.equipment.models import InuitsEquipment
from apps.equipment.models.fields import InuitsEquipmentNonMemberRelatedField

from scouts_auth.groupadmin.serializers import ScoutsMemberSearchFrontendSerializer
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.serializers.fields import OptionalCharField


logger = logging.getLogger(__name__)


class InuitsEquipmentSerializer(serializers.ModelSerializer):

    LBL_OWNER_MEMBER = "owner_member_group_admin_id"
    LBL_OWNER_GROUP = "owner_group_group_admin_id"

    # inuits_equipment_id           pk
    # nature                        max_length=50                   is optional
    # description                   max_length=500                  is optional
    # total_value                   decimal field
    # owner_non_member              references InuitsNonMember
    # owner_member_group_admin_id   group admin id of owner member
    # owner_group_group_admin_id    group admin id of owner group

    owner_non_member = InuitsEquipmentNonMemberRelatedField(required=False, allow_null=True)
    owner_member_group_admin_id = OptionalCharField()
    owner_group_group_admin_id = OptionalCharField()

    class Meta:
        model = InuitsEquipment
        fields = (
            "id",
            "nature",
            "description",
            "total_value",
            "owner_non_member",
            "owner_member_group_admin_id",
            "owner_group_group_admin_id",
        )

    def to_internal_value(self, data: dict) -> dict:
        data[InuitsEquipmentSerializer.LBL_OWNER_GROUP] = data.pop("owner_group", None)
        data[InuitsEquipmentSerializer.LBL_OWNER_MEMBER] = data.pop("owner_member", None)

        return data

    def validate(self, data):
        logger.debug("SERIALIZER VALIDATE DATA: %s", data)

        owner_non_member = data.get("owner_non_member", None)
        owner_member = data.get(InuitsEquipmentSerializer.LBL_OWNER_MEMBER, None)
        owner_group = data.get(InuitsEquipmentSerializer.LBL_OWNER_GROUP, None)

        if not owner_member and not owner_non_member and not owner_group:
            raise serializers.ValidationError("A piece of equipment needs an owner")
        if owner_member and owner_non_member and owner_group:
            raise serializers.ValidationError("There can only be one owner of the piece of equipment")
        if owner_group and (owner_member or owner_non_member):
            logger.warn(
                "A piece of equipment either belongs to a person or to a scouts group - Removing group as owner"
            )
            data[InuitsEquipmentSerializer.LBL_OWNER_GROUP] = ""
        return data

    # @swagger_serializer_method(serializer_or_field=ScoutsMemberSearchFrontendSerializer)
    # def get_owner_member(self, obj):
    #     if not obj.owner_member_group_admin_id:
    #         return None
    #     request = self.context.get("request", None)
    #     return ScoutsMemberSearchFrontendSerializer(
    #         GroupAdmin().get_member_info(active_user=request.user, group_admin_id=obj.owner_member_group_admin_id)
    #     ).data

    # @swagger_serializer_method(serializer_or_field=owner_group)
    # def get_owner_group(self, obj):
    #     logger.debug("OBJ: %s", obj)
    #     return obj.owner_group_group_admin_id
