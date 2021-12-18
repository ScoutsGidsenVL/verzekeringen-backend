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
        equipment: List[InuitsEquipment],
        **base_insurance_fields,
    ) -> EquipmentInsurance:
        
        # Create the insurance
        insurance = self.equipment_insurance_create(
            *args,
            **base_insurance_fields,
        )
        
        # Save the equipment instances and link them in a template
        for inuits_equipment in equipment:
            # Update if necessary
            inuits_equipment.full_clean()
            inuits_equipment.save()
            
            equipment = self.equipment_service.equipment_create(insurance, inuits_equipment.description, inuits_equipment.total_value, inuits_equipment.nature)
            
            
        

        self.base_insurance_service.handle_insurance_created(insurance)
        
        return insurance

