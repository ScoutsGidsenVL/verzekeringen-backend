import logging
from decimal import Decimal

from django.conf import settings
from django.db import transaction

from apps.equipment.models import InuitsEquipment
from apps.people.models import InuitsNonMember

from scouts_auth.groupadmin.models import AbstractScoutsGroup, AbstractScoutsMember


logger = logging.getLogger(__name__)


class InuitsEquipmentService:
    @transaction.atomic
    def inuits_equipment_create(
        self,
        description: str,
        total_value: Decimal,
        created_by: settings.AUTH_USER_MODEL,
        nature: str = None,
        owner_group: AbstractScoutsGroup = None,
        owner_non_member: InuitsNonMember = None,
        owner_member: AbstractScoutsMember = None,
    ) -> InuitsEquipment:
        equipment = InuitsEquipment(
            nature=nature,
            description=description,
            total_value=total_value,
            owner_group=owner_group.group_admin_id if owner_group else None,
            owner_non_member=owner_non_member,
            owner_member=owner_member.group_admin_id if owner_member else None,
        )

        equipment.full_clean()
        equipment.save()

        return equipment

    @transaction.atomic
    def inuits_equipment_update(self, *, equipment: InuitsEquipment, **fields) -> InuitsEquipment:
        equipment.nature = fields.get("nature", equipment.nature)
        equipment.description = fields.get("description", equipment.description)
        equipment.total_value = fields.get("total_value", equipment.total_value)
        equipment.owner_non_member = fields.get("owner_non_member", equipment.owner_non_member)
        equipment.owner_member = fields.get("owner_member", equipment.owner_member)
        equipment.owner_group = fields.get("owner_group", equipment.owner_group)

        equipment.full_clean()
        equipment.save()

        return equipment
