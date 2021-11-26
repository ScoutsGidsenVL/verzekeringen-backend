import logging
from decimal import Decimal

from django.db import transaction

from scouts_insurances.people.services import MemberService
from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import EquipmentInsurance


logger = logging.getLogger(__name__)


class EquipmentService:
    member_service = MemberService()

    @transaction.atomic
    def equipment_create(
        self,
        *,
        insurance: EquipmentInsurance,
        description: str,
        total_value: Decimal,
        nature: str = None,
        owner_non_member: dict = None,
        owner_member: dict = None,
        id: str = None,
        inuits_equipment_id: str = None,
    ) -> Equipment:
        equipment = Equipment(nature=nature, description=description, total_value=total_value, insurance=insurance)
        if owner_non_member:
            equipment.owner_non_member = self.member_service.non_member_create(**owner_non_member)
        if owner_member:
            equipment.owner_member = self.member_service.member_create(**owner_member)
        equipment.full_clean()
        equipment.save()

        # # InuitsEquipment is created in the sidebar and should already be there.
        # if not inuits_equipment_id:
        #     raise ValidationError("Inuits equipment id must be provided")
        # else:
        #     inuits_equipment = InuitsEquipment.objects.all().get(pk=inuits_equipment_id)

        #     if not inuits_equipment:
        #         raise ValidationError("Couldn't find InuitsEquipment instance with %s", str(inuits_equipment_id))
        #     else:
        #         equipment_inuits_template = EquipmentInuitsTemplate(
        #             equipment=equipment, inuits_equipment=inuits_equipment
        #         )
        #         equipment_inuits_template.full_clean()
        #         equipment_inuits_template.save()

        return equipment

    def equipment_update(
        self,
        *,
        insurance=EquipmentInsurance,
        equipment: Equipment,
        description: str = None,
        total_value: Decimal = None,
        nature: str = None,
        owner_non_member: dict = None,
        owner_member: dict = None,
        inuits_equipment_id: str = None,
        id: str = None,
    ) -> Equipment:
        equipment.insurance = insurance
        equipment.nature = nature if nature else equipment.nature
        equipment.description = description if description else equipment.description
        equipment.total_value = total_value if total_value else equipment.total_value
        equipment.owner_non_member = owner_non_member if owner_non_member else equipment.owner_non_member
        equipment.owner_member = owner_member if owner_member else equipment.owner_member

        equipment.full_clean()
        equipment.save()

        return equipment

    def equipment_create_or_update(
        self,
        *,
        insurance: EquipmentInsurance,
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
            return self.equipment_update(
                insurance=insurance,
                equipment=equipment,
                description=description,
                total_value=total_value,
                nature=nature,
                owner_non_member=owner_non_member,
                owner_member=owner_member,
                inuits_equipment_id=inuits_equipment_id,
            )
        else:
            logger.debug("Creating Equipment instance with inuits_equipment_id %s", inuits_equipment_id)
            return self.equipment_create(
                insurance=insurance,
                description=description,
                total_value=total_value,
                nature=nature,
                owner_non_member=owner_non_member,
                owner_member=owner_member,
                inuits_equipment_id=inuits_equipment_id,
            )
