import logging

from django.conf import settings
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from apps.people.services import InuitsNonMemberService
from apps.equipment.models import InuitsEquipment, InuitsEquipmentTemplate

from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import EquipmentInsurance

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_insurances.people.models import NonMember, Member
from scouts_insurances.people.services.member_service import MemberService

logger = logging.getLogger(__name__)


class InuitsEquipmentService:
    non_member_service = InuitsNonMemberService()
    member_service = MemberService()

    @transaction.atomic
    def inuits_equipment_create(
            self, inuits_equipment: InuitsEquipment, created_by: settings.AUTH_USER_MODEL
    ) -> InuitsEquipment:
        # Check if the instance already exists
        create = True
        if inuits_equipment.has_id():
            try:
                logger.debug("QUERYING FOR INUITS EQUIPMENT WITH ID: %s", inuits_equipment.id)
                object = InuitsEquipment.objects.get(pk=inuits_equipment.id)
                if object:
                    logger.debug("INUITS EQUIPMENT ALREADY EXISTS: %s", inuits_equipment)
                    create = False
                    # return inuits_equipment
                    # return self.inuits_equipment_update(
                    #     inuits_equipment=inuits_equipment, updated_inuits_equipment=object, updated_by=created_by
                    # )
            except ObjectDoesNotExist:
                pass

        if inuits_equipment.owner_non_member:
            logger.debug(
                "INUITS EQUIPMENT OWNER_NON_MEMBER: %s (%s)",
                inuits_equipment.owner_non_member,
                type(inuits_equipment.owner_non_member).__name__,
            )
            self.non_member_service.linked_non_member_create(
                inuits_non_member=inuits_equipment.owner_non_member, created_by=created_by
            )

        if create:
            logger.debug(
                "INUITS EQUIPMENT WILL BE CREATED: %s (%s)", inuits_equipment, type(inuits_equipment).__name__
            )
            inuits_equipment = InuitsEquipment(
                nature=inuits_equipment.nature,
                description=inuits_equipment.description,
                total_value=inuits_equipment.total_value,
                owner_group=inuits_equipment.owner_group.group_admin_id if inuits_equipment.owner_group else None,
                owner_non_member=inuits_equipment.owner_non_member,
                owner_member=inuits_equipment.owner_member.group_admin_id if inuits_equipment.owner_member else None,
                created_by=created_by,
            )

            inuits_equipment.full_clean()
            inuits_equipment.save()

        return inuits_equipment

    @transaction.atomic
    def linked_equipment_create(
            self, insurance: EquipmentInsurance, inuits_equipment: InuitsEquipment, created_by: settings.AUTH_USER_MODEL
    ) -> Equipment:
        """
        Creates an Equipment instance.
        """
        inuits_equipment = self.inuits_equipment_create(inuits_equipment=inuits_equipment, created_by=created_by)

        equipment = self.equipment_create(insurance=insurance, inuits_equipment=inuits_equipment)

        equipment_template = InuitsEquipmentTemplate()
        equipment_template.equipment = equipment
        equipment_template.inuits_equipment = inuits_equipment
        equipment_template.full_clean()
        equipment_template.save()

        return equipment

    @transaction.atomic
    def equipment_create(
            self,
            insurance: EquipmentInsurance,
            inuits_equipment: InuitsEquipment,
    ) -> Equipment:
        equipment = Equipment(
            inuits_id=inuits_equipment.id,
            nature=inuits_equipment.nature,
            insurance=insurance,
            description=inuits_equipment.description,
            total_value=inuits_equipment.total_value,
        )
        if inuits_equipment.owner_non_member:
            equipment.owner_non_member = self.non_member_service.non_member_create(inuits_equipment.owner_non_member)
        if inuits_equipment.owner_member:
            equipment.owner_member = self.member_service.member_create(
                first_name=inuits_equipment.owner_member.first_name,
                last_name=inuits_equipment.owner_member.last_name,
                phone_number=inuits_equipment.owner_member.phone_number,
                birth_date=inuits_equipment.owner_member.birth_date,
                email=inuits_equipment.owner_member.email,
                membership_number=inuits_equipment.owner_member.membership_number,
                group_admin_id=inuits_equipment.owner_member.group_admin_id
            )
        equipment.full_clean()
        equipment.save()

        return equipment

    @transaction.atomic
    def inuits_equipment_update(
            self,
            *,
            inuits_equipment: InuitsEquipment,
            updated_inuits_equipment: InuitsEquipment,
            updated_by: settings.AUTH_USER_MODEL,
    ) -> InuitsEquipment:
        # logger.debug("UPDATED EQUIPMENT: %s", updated_inuits_equipment)
        if inuits_equipment.equals(updated_inuits_equipment):
            return updated_inuits_equipment

        # Update the InuitsNonMember instance
        inuits_equipment.nature = (
            updated_inuits_equipment.nature if updated_inuits_equipment.nature else inuits_equipment.nature
        )
        inuits_equipment.description = (
            updated_inuits_equipment.description
            if updated_inuits_equipment.description
            else inuits_equipment.description
        )
        inuits_equipment.total_value = (
            updated_inuits_equipment.total_value
            if updated_inuits_equipment.total_value
            else inuits_equipment.total_value
        )
        inuits_equipment.owner_non_member = (
            updated_inuits_equipment.owner_non_member
            if updated_inuits_equipment.owner_non_member
            else None
        )
        inuits_equipment.owner_member = (
            updated_inuits_equipment.owner_member.group_admin_id
            if updated_inuits_equipment.owner_member
            else None
        )
        if updated_inuits_equipment.owner_group:
            if isinstance(updated_inuits_equipment.owner_group, AbstractScoutsGroup):
                inuits_equipment.owner_group = updated_inuits_equipment.owner_group.group_admin_id
            else:
                inuits_equipment.owner_group = updated_inuits_equipment.owner_group
        else:
            inuits_equipment.owner_group = updated_inuits_equipment.owner_group

        inuits_equipment.updated_by = updated_by

        inuits_equipment.full_clean()
        inuits_equipment.save()

        # Check to see if the scouts Equipment instance can also be updated
        equipment = InuitsEquipmentTemplate.objects.all().filter(
            inuits_equipment=inuits_equipment, equipment__in=list(Equipment.objects.all().editable(user=None))
        )
        # logger.debug("EQUIPMENT: %s", equipment)

        for item in equipment:
            self.equipment_update(equipment=item.equipment, updated_equipment=inuits_equipment)

        return inuits_equipment

    @transaction.atomic
    def equipment_update(
            self,
            *,
            equipment: Equipment,
            updated_equipment: InuitsEquipment,
    ) -> Equipment:
        # equipment.insurance = insurance
        equipment.nature = (
            updated_equipment.nature if updated_equipment.nature and not updated_equipment.owner_member else None if updated_equipment.owner_member else equipment.nature
        )
        equipment.description = (
            updated_equipment.description if updated_equipment.description else equipment.description
        )
        equipment.total_value = (
            updated_equipment.total_value if updated_equipment.total_value else equipment.total_value
        )
        owner_non_member = NonMember.objects.all().filter(inuits_id=updated_equipment.owner_non_member.id).last() if updated_equipment.owner_non_member else None
        equipment.owner_non_member = (
            owner_non_member
        )
        owner_member = Member.objects.filter(group_admin_id=updated_equipment.owner_member if isinstance(updated_equipment.owner_member, str) else updated_equipment.owner_member.group_admin_id).last() if updated_equipment.owner_member else None
        equipment.owner_member = owner_member

        equipment.owner_group = (
            updated_equipment.owner_group if updated_equipment.owner_group else equipment.owner_group
        )

        equipment.full_clean()
        equipment.save()

        return equipment
