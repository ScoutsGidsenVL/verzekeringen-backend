import logging

from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.equipment.models import InuitsEquipment
from apps.equipment.models.fields import InuitsEquipmentNonMemberRelatedField

from groupadmin.serializers import ScoutsMemberSearchFrontendSerializer
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsEquipmentSerializer(serializers.ModelSerializer):

    # inuits_equipment_id           pk
    # nature                        max_length=50                   is optional
    # description                   max_length=500                  is optional
    # total_value                   decimal field
    # owner_non_member              references InuitsNonMember
    # owner_member_group_admin_id   group admin id of owner member
    # owner_group_group_admin_id    group admin id of owner group

    owner_non_member = InuitsEquipmentNonMemberRelatedField()
    owner_member = serializers.SerializerMethodField()
    owner_group = serializers.CharField(source="owner_group_group_admin_id", required=False, allow_blank=True)

    class Meta:
        model = InuitsEquipment
        fields = (
            "inuits_equipment_id",
            "nature",
            "description",
            "total_value",
            "owner_non_member",
            "owner_member",
            "owner_group",
        )

    def validate(self, data):
        if not data.get("owner_member") and not data.get("owner_non_member") and not data.get("owner_group"):
            raise serializers.ValidationError("A piece of equipment needs an owner")
        if data.get("owner_member") and data.get("owner_non_member") and data.get("owner_group"):
            raise serializers.ValidationError("There can only be one owner of the piece of equipment")
        if data.get("owner_group") and (data.get("owner_member") or data.get("owner_non_member")):
            logger.warn(
                "A piece of equipment either belongs to a person or to a scouts group - Removing group as owner"
            )
            data["owner_group"] = ""
        return data

    @swagger_serializer_method(serializer_or_field=ScoutsMemberSearchFrontendSerializer)
    def get_owner_member(self, obj):
        if not obj.owner_member_group_admin_id:
            return None
        request = self.context.get("request", None)
        return ScoutsMemberSearchFrontendSerializer(
            GroupAdmin().get_member_info(active_user=request.user, group_admin_id=obj.owner_member_group_admin_id)
        ).data
