import logging
from typing import List

from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.core.exceptions import ValidationError

from apps.equipment.models import InuitsEquipment
from apps.equipment.services import InuitsEquipmentService

from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.services import BaseInsuranceService, EquipmentInsuranceService


logger = logging.getLogger(__name__)


class InuitsEquipmentInsuranceService(EquipmentInsuranceService):
    base_insurance_service = BaseInsuranceService()
    equipment_service = InuitsEquipmentService()

    @transaction.atomic
    def inuits_equipment_insurance_create(
        self,
        *args,
        **base_insurance_fields,
    ) -> EquipmentInsurance:
        equipment = base_insurance_fields.pop("equipment", [])

        # Create the insurance
        insurance = self.equipment_insurance_create(
            *args,
            **base_insurance_fields,
        )

        # Save the equipment instances and link them in a template
        for item in equipment:
            # Update if necessary
            # item.full_clean()
            # item.save()

            item = self.equipment_service.linked_equipment_create(
                insurance=insurance, inuits_equipment=item, created_by=base_insurance_fields.get("created_by")
            )

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def inuits_equipment_insurance_update(self, *, insurance: EquipmentInsurance, **fields) -> EquipmentInsurance:
        insurance.start_date = fields.get("start_date", insurance.start_date)
        insurance.end_date = fields.get("end_date", insurance.end_date)
        insurance.nature = fields.get("nature", insurance.nature)
        insurance.postal_code = fields.get("postal_code", insurance.postal_code)
        insurance.city = fields.get("city", insurance.city)

        insurance.full_clean()
        insurance.save()

        # The equipment list contains instances that are already persisted in InuitsEquipment
        # No need to update the InuitsEquipment instances, only the linked Equipment instances.
        self._update_equipment(
            insurance=insurance, inuits_equipment_list=fields.get("equipment", []), created_by=fields.get("created_by")
        )

        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()

        insurance.save()

    def _update_equipment(
        self,
        insurance: EquipmentInsurance,
        inuits_equipment_list: List[InuitsEquipment],
        created_by: settings.AUTH_USER_MODEL,
    ):
        insurance_equipment_list: List[Equipment] = insurance.equipment.all()
        updated_insurance_equipment_list: List[Equipment] = []

        # First update the list of equipment that was submitted
        for inuits_equipment in inuits_equipment_list:
            equipment = Equipment.objects.filter(
                Q(insurance=insurance) & Q(template__inuits_equipment=inuits_equipment)
            ).last()

            logger.debug("INUITS EQUIPMENT TO UPDATE: %s", inuits_equipment)
            logger.debug("EQUIPMENT TO UPDATE: %s", equipment)

            if not equipment:
                equipment = self.equipment_service.linked_equipment_create(
                    insurance=insurance, inuits_equipment=inuits_equipment, created_by=created_by
                )

            equipment = self.equipment_service.equipment_update(
                equipment=equipment, updated_equipment=inuits_equipment
            )

            updated_insurance_equipment_list.append(equipment)

        # Now check for deleted items
        for equipment in insurance_equipment_list:
            if not equipment in updated_insurance_equipment_list:
                logger.debug("Removing (%s) from the insurance equipment list", equipment)

                # A constraint on the equipment table prevents setting the insurance id to null
                # Otherwise, we could have just done:
                #
                # insurance.equipment.remove(equipment)
                #
                # and then checked if the equipment was used elsewhere and possibly remove it altogether.
                # Since that's not an option, we'll just delete the equipment instance altogether
                equipment.delete()

    # def update_equipment(self, insurance: EquipmentInsurance, equipment: list):
    #     # If a piece of equipment was removed from the list, also remove it from the database.
    #     # Make sure the equipment is not part of an insurance request that is not new or waiting (i.e. already approved or billed).
    #     logger.debug("Updating equipment list on insurance %s", insurance.id)
    #     existing_equipment_list = [
    #         equipment.id
    #         for equipment in Equipment.objects.filter(
    #             Q(insurance=insurance)
    #             & Q(insurance__insurance_parent___status__in=[InsuranceStatus.NEW, InsuranceStatus.WAITING])
    #         )
    #     ]

    #     logger.debug(
    #         "List of existing equipment for insurance %s that are not NEW or WAITING: %s",
    #         insurance.id,
    #         existing_equipment_list,
    #     )

    #     for equipment_data in equipment:
    #         equipment_id = equipment_data.get("id", None)
    #         inuits_equipment_id = equipment_data.get("inuits_equipment_id", None)

    #         equipment = self.equipment_service.equipment_create_or_update(**equipment_data, insurance=insurance)

    #         if equipment_id and equipment_id in existing_equipment_list:
    #             existing_equipment_list.remove(equipment.id)

    #     for equipment_id in existing_equipment_list:
    #         logger.debug("Deleting unused equipment %s from insurance %s", equipment_id, insurance.id)
    #         equipment = Equipment.objects.get(pk=equipment_id)

    #         equipment.delete()
