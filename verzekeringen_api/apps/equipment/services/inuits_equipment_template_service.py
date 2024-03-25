import logging
from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction

from apps.equipment.models import InuitsEquipment, InuitsEquipmentTemplate
from apps.equipment.services import InuitsEquipmentService
from apps.people.models import InuitsNonMember

logger = logging.getLogger(__name__)


class InuitsEquipmentTemplateService:
    service = InuitsEquipmentService()

    @transaction.atomic
    def inuits_equipment_template_create(
        self,
        *,
        description: str,
        total_value: Decimal,
        created_by: settings.AUTH_USER_MODEL,
        nature: str = None,
        owner_group_group_admin_id: str = None,
        owner_non_member: InuitsNonMember = None,
        owner_member_group_admin_id: str = None,
    ) -> InuitsEquipmentTemplate:
        inuits_equipment: InuitsEquipment = self.service.inuits_equipment_create(
            description=description,
            total_value=total_value,
            created_by=created_by,
            nature=nature,
            owner_group_group_admin_id=owner_group_group_admin_id,
            owner_non_member=owner_non_member,
            owner_member_group_admin_id=owner_member_group_admin_id,
        )

        template: InuitsEquipmentTemplate = InuitsEquipmentTemplate(inuits_equipment=inuits_equipment)

        template.full_clean()
        template.save()

        return template

    @transaction.atomic
    def inuits_equipment_template_update(self, *, equipment: InuitsEquipment, **fields) -> InuitsEquipment:
        equipment.nature = fields.get("nature", equipment.nature)
        equipment.description = fields.get("description", equipment.description)
        equipment.total_value = fields.get("total_value", equipment.total_value)
        equipment.owner_non_member = fields.get("owner_non_member", equipment.owner_non_member)
        equipment.owner_member_group_admin_id = fields.get(
            "owner_member_group_admin_id", equipment.owner_member_group_admin_id
        )
        equipment.owner_group_group_admin_id = fields.get(
            "owner_group_group_admin_id", equipment.owner_group_group_admin_id
        )

        equipment.full_clean()
        equipment.save()

        return equipment
