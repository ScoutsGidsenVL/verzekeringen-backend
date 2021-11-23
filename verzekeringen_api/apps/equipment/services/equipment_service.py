import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ValidationError

from apps.members.models import InuitsNonMember
from apps.members.services import MemberService
from apps.equipment.models import Equipment, InuitsEquipment, EquipmentInuitsTemplate
from apps.insurances.models import EquipmentInsurance


logger = logging.getLogger(__name__)


def inuits_equipment_create(
    *,
    description: str,
    total_value: Decimal,
    created_by: settings.AUTH_USER_MODEL,
    nature: str = None,
    owner_group: str = None,
    owner_non_member: InuitsNonMember = None,
    owner_member: str = None,
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
        owner_member_group_admin_id=owner_member,
    )

    equipment.full_clean()
    equipment.save()

    return equipment


def inuits_equipment_update(*, equipment: InuitsEquipment, **fields) -> InuitsEquipment:
    equipment.nature = fields.get("nature", equipment.nature)
    equipment.description = fields.get("description", equipment.description)
    equipment.total_value = fields.get("total_value", equipment.total_value)
    equipment.owner_non_member = fields.get("owner_non_member", equipment.owner_non_member)
    equipment.owner_member_group_admin_id = fields.get("owner_member", equipment.owner_member_group_admin_id)
    equipment.owner_group_group_admin_id = fields.get("owner_group", equipment.owner_group_group_admin_id)

    equipment.full_clean()
    equipment.save()

    return equipment


@transaction.atomic
def equipment_create(
    *,
    insurance,
    description: str,
    total_value: Decimal,
    nature: str = None,
    owner_non_member: dict = None,
    owner_member: dict = None,
    inuits_equipment_id: str = None,
) -> Equipment:
    equipment = Equipment(nature=nature, description=description, total_value=total_value, insurance=insurance)
    if owner_non_member:
        equipment.owner_non_member = MemberService.non_member_create(**owner_non_member)
    if owner_member:
        equipment.owner_member = MemberService.member_create(**owner_member)
    equipment.full_clean()
    equipment.save()

    # InuitsEquipment is created in the sidebar and should already be there.
    if not inuits_equipment_id:
        raise ValidationError("Inuits equipment id must be provided")
    else:
        inuits_equipment = InuitsEquipment.objects.all().get(pk=inuits_equipment_id)

        if not inuits_equipment:
            raise ValidationError("Couldn't find InuitsEquipment instance with %s", str(inuits_equipment_id))
        else:
            equipment_inuits_template = EquipmentInuitsTemplate(equipment=equipment, inuits_equipment=inuits_equipment)
            equipment_inuits_template.full_clean()
            equipment_inuits_template.save()

    return equipment


def equipment_update(
    *,
    equipment: Equipment,
    insurance=EquipmentInsurance,
    description: str = None,
    total_value: Decimal = None,
    nature: str = None,
    owner_non_member: dict = None,
    owner_member: dict = None,
    inuits_equipment_id: str = None,
    id: str = None,
) -> Equipment:
    equipment.nature = nature if nature else equipment.nature
    equipment.description = description if description else equipment.description
    equipment.total_value = total_value if total_value else equipment.total_value
    equipment.owner_non_member = owner_non_member if owner_non_member else equipment.owner_non_member
    equipment.owner_member = owner_member if owner_member else equipment.owner_member

    equipment.full_clean()
    equipment.save()

    return equipment


def equipment_create_or_update(
    *,
    insurance,
    description: str,
    total_value: Decimal,
    nature: str = None,
    owner_non_member: dict = None,
    owner_member: dict = None,
    inuits_equipment_id: str = None,
    id: str = None,
) -> Equipment:
    equipment = None
    if id:
        try:
            equipment = Equipment.objects.get(pk=id)
        except Exception:
            pass

    if equipment:
        logger.debug(
            "Updating Equipment instance with id %s and inuits_equipment_id %s", equipment.id, inuits_equipment_id
        )
        return equipment_update(
            equipment=equipment,
            insurance=insurance,
            description=description,
            total_value=total_value,
            nature=nature,
            owner_non_member=owner_non_member,
            owner_member=owner_member,
            inuits_equipment_id=inuits_equipment_id,
        )
    else:
        logger.debug("Creating Equipment instance with inuits_equipment_id %s", inuits_equipment_id)
        return equipment_create(
            insurance=insurance,
            description=description,
            total_value=total_value,
            nature=nature,
            owner_non_member=owner_non_member,
            owner_member=owner_member,
            inuits_equipment_id=inuits_equipment_id,
        )
