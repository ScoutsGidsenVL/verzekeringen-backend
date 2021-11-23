from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.members.models import InuitsNonMember
from apps.members.services import MemberService
from apps.equipment.models import Equipment, InuitsEquipment


def inuits_equipment_create(
    *,
    description: str,
    total_value: Decimal,
    created_by: settings.AUTH_USER_MODEL,
    nature: str = None,
    owner_group: str = None,
    owner_non_member: InuitsNonMember = None,
    owner_member_id: str = None,
) -> InuitsEquipment:
    # validate group
    if owner_group not in (group.group_admin_id for group in created_by.scouts_groups):
        raise ValidationError("Given group %s is not a valid group of user" % owner_group)
    equipment = InuitsEquipment(
        nature=nature,
        description=description,
        total_value=total_value,
        owner_group_group_admin_id=owner_group,
        owner_non_member=owner_non_member,
        owner_member_group_admin_id=owner_member_id,
    )

    equipment.full_clean()
    equipment.save()

    return equipment


def inuits_equipment_update(*, equipment: InuitsEquipment, **fields) -> InuitsEquipment:
    equipment.nature = fields.get("nature", equipment.nature)
    equipment.description = fields.get("description", equipment.description)
    equipment.total_value = fields.get("total_value", equipment.total_value)
    equipment.owner_non_member = fields.get("owner_non_member", equipment.owner_non_member)
    equipment.owner_member_group_admin_id = fields.get("owner_member_id", equipment.owner_member_group_admin_id)
    equipment.owner_group_group_admin_id = fields.get("owner_group", equipment.group_group_admin_id)

    equipment.full_clean()
    equipment.save()

    return equipment


@transaction.atomic
def equipment_create(
    *,
    description: str,
    total_value: Decimal,
    insurance,
    nature: str = None,
    owner_non_member: dict = None,
    owner_member: dict = None,
) -> Equipment:
    equipment = Equipment(nature=nature, description=description, total_value=total_value, insurance=insurance)
    if owner_non_member:
        equipment.owner_non_member = MemberService.non_member_create(**owner_non_member)
    if owner_member:
        equipment.owner_member = MemberService.member_create(**owner_member)
    equipment.full_clean()
    equipment.save()

    return equipment
