import logging
from typing import List

from django.db import transaction

from apps.equipment.models import InuitsEquipment
from apps.equipment.services import InuitsEquipmentService

from scouts_insurances.equipment.models import Equipment
from scouts_insurances.equipment.services import EquipmentService
from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.services import BaseInsuranceService, EquipmentInsuranceService


logger = logging.getLogger(__name__)


class InuitsEquipmentInsuranceService(EquipmentInsuranceService):
    base_insurance_service = BaseInsuranceService()
    inuits_equipment_service = InuitsEquipmentService()
    equipment_service = EquipmentService()

    @transaction.atomic
    def inuits_equipment_insurance_create(
        self,
        *args,
        inuits_equipment: List[InuitsEquipment],
        **base_insurance_fields,
    ) -> EquipmentInsurance:

        # Create the insurance
        insurance = self.equipment_insurance_create(
            *args,
            **base_insurance_fields,
        )

        # Save the equipment instances and link them in a template
        for item in inuits_equipment:
            # Update if necessary
            item.full_clean()
            item.save()

            equipment = self.equipment_service.equipment_create(
                insurance, item.description, item.total_value, item.nature, owner_non_member, owner_member
            )

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance
