import logging

from rest_framework import serializers

from apps.equipment.models import InuitsEquipment
from apps.people.models import InuitsNonMember
from apps.people.serializers import InuitsNonMemberSerializer
from apps.people.serializers.fields import InuitsNonMemberSerializerField

from scouts_auth.groupadmin.models import AbstractScoutsMember, AbstractScoutsGroup
from scouts_auth.groupadmin.serializers.fields import (
    AbstractScoutsMemberSerializerField,
    AbstractScoutsGroupSerializerField,
)

logger = logging.getLogger(__name__)


class InuitsEquipmentSerializer(serializers.ModelSerializer):
    serialize = True

    # id                            pk
    # nature                        max_length=50                   is optional
    # description                   max_length=500                  is optional
    # total_value                   decimal field
    # owner_non_member              references InuitsNonMember
    # owner_member_group_admin_id   group admin id of owner member
    # owner_group_group_admin_id    group admin id of owner group

    # owner_non_member = InuitsEquipmentNonMemberRelatedField(required=False, allow_null=True)
    owner_non_member = InuitsNonMemberSerializerField(required=False, allow_null=True)
    # owner_non_member = InuitsNonMemberSerializer()
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

    def to_internal_value(self, data: dict):
        owner_non_member = data.get("owner_non_member", None)
        if not isinstance(owner_non_member, str) and owner_non_member and owner_non_member.get("inuits_id", None):
            data["owner_non_member"] = owner_non_member.get("inuits_id", None)
            inuits_equipment = InuitsEquipment.objects.all().filter(template__equipment=data.get("id", None)).last()
            if inuits_equipment:
                data["id"] = inuits_equipment.id
        id = data.get("id", None)
        logger.debug("INUITS EQUIPMENT SERIALIZER DATA: %s", data)

        group_admin_id = data.get("group_admin_id", data.get("group_group_admin_id", None))
        owner_non_member = data.get("owner_non_member", None)
        owner_member = data.get("owner_member", None)
        owner_group = data.get("owner_group", None)

        if owner_non_member or owner_member:
            data.pop("owner_group", None)
        else:
            data["owner_group"] = owner_group if owner_group else group_admin_id

        data = super().to_internal_value(data)

        data["id"] = id

        logger.debug("INUITS EQUIPMENT INTERNALIZED DATA: %s", data)

        return data

    def to_representation(self, data: dict) -> dict:
        logger.debug("INUITS EQUIPMENT REPRESENTATION DATA: %s (%s)", data, type(data).__name__)
        # HACKETY HACK
        inuits_equipment = InuitsEquipment.objects.all().filter(template__equipment=data.id).last()

        if inuits_equipment:
            data.id = inuits_equipment.id

        return super().to_representation(data)

    def validate(self, data: dict) -> InuitsEquipment:
        # @TODO should be either one, not both
        group_admin_id = data.get("group_admin_id", data.get("group_group_admin_id", None))
        owner_non_member = data.get("owner_non_member", None)
        owner_member = data.get("owner_member", None)
        owner_group = data.get("owner_group", None)

        logger.debug("INUITS EQUIPMENT VALIDATE DATA: %s", data)

        if not owner_member and not owner_non_member and not owner_group:
            if not group_admin_id:
                raise serializers.ValidationError("A piece of equipment needs an owner")
            owner_group = group_admin_id
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

        # if owner_group and not isinstance(owner_group, AbstractScoutsGroup):
        #     raise serializers.ValidationError(
        #         "AbstractScoutsGroup instance couldn't be loaded with the provided group admin id"
        #     )

        data = InuitsEquipment(**data)

        logger.debug("VALIDATE OBJECT: %s", data)

        return data
