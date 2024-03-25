import logging
from decimal import Decimal
from typing import List

from django.db import transaction
from django.db.models import Q

from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import CostVariable, EquipmentInsurance, InsuranceType
from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.insurances.services import BaseInsuranceService
from scouts_insurances.locations.models import Country

logger = logging.getLogger(__name__)


class EquipmentInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: EquipmentInsurance, equipment_list: List[Equipment] = []) -> Decimal:
        equipment_cost = 0

        if not equipment_list:
            equipment_list = insurance.equipment.all()

        for equipment in equipment_list:
            equipment_cost += equipment.amount * equipment.total_value

        cost = equipment_cost * CostVariable.objects.get_variable(insurance.type, "premium_percentage").value
        if cost < CostVariable.objects.get_variable(insurance.type, "premium_minimum").value:
            cost = CostVariable.objects.get_variable(insurance.type, "premium_minimum").value

        return round(cost, 2)

    # We create an insurance in memory (! so no saving) and calculate cost
    def equipment_insurance_cost_calculation(
        self,
        *,
        nature: str,
        equipment: list,
        postal_code: int = None,
        city: str = None,
        country: str = None,
        **base_insurance_fields,
    ) -> Decimal:
        type = InsuranceType.objects.equipment()
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
        country = country if country and isinstance(country, str) else Country.DEFAULT_COUNTRY_NAME
        insurance = EquipmentInsurance(
            nature=nature,
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        insurance.country = Country.objects.by_insurance_type_id(InsuranceTypeEnum.EQUIPMENT).get(name=country).name

        # Create some fake equipment data for cost calc (only need total value)
        equipment_objects = []
        for equipment_data in equipment:
            equipment_objects.append(Equipment(total_value=equipment_data.total_value))
        return self._calculate_total_cost(insurance, equipment_objects)

    @transaction.atomic
    def equipment_insurance_create(
        self,
        *,
        nature: str,
        postal_code: int = None,
        city: str = None,
        country: str = None,
        **base_insurance_fields,
    ) -> EquipmentInsurance:
        type = InsuranceType.objects.equipment()
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
        insurance = EquipmentInsurance(
            nature=nature,
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        insurance.country = country
        # We can only calculate after equipments added so for now add 0
        insurance.total_cost = 0
        insurance.full_clean()
        insurance.save()

        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()

        return insurance

    @transaction.atomic
    def equipment_insurance_delete(self, *, insurance: EquipmentInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.equipment.clear()
        insurance.delete()
