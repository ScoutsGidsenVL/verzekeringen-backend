from django.db import transaction
from decimal import Decimal
from django.conf import settings
from apps.equipment.services import EquipmentService
from apps.equipment.models import Equipment
from apps.locations.utils import PostcodeCity
from ..models import EquipmentInsurance, InsuranceType, CostVariable
from . import base_insurance_service as BaseInsuranceService


def _calculate_total_cost(insurance: EquipmentInsurance, equipment_list: list = []) -> Decimal:
    equipment_cost = 0

    if not equipment_list:
        equipment_list = insurance.equipment.all()

    for equipment in equipment_list:
        equipment_cost += equipment._amount * equipment.total_value

    cost = equipment_cost * CostVariable.objects.get_variable(insurance.type, "premium_percentage").value
    if cost < CostVariable.objects.get_variable(insurance.type, "premium_minimum").value:
        cost = CostVariable.objects.get_variable(insurance.type, "premium_minimum").value

    return round(cost, 2)


# We create an insurance in memory (! so no saving) and calculate cost
def equipment_insurance_cost_calculation(
    *,
    nature: str,
    equipment: list,
    postcode_city: PostcodeCity = None,
    country: str = None,
    **base_insurance_fields,
) -> Decimal:
    type = InsuranceType.objects.equipment()
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(**base_insurance_fields, type=type)
    insurance = EquipmentInsurance(
        nature=nature,
        postcode=int(postcode_city.postcode) if postcode_city else None,
        city=postcode_city.name if postcode_city else None,
        **base_insurance_fields,
    )
    insurance.country = country
    # Create some fake equipment data for cost calc (only need total value)
    equipment_objects = []
    for equipment_data in equipment:
        equipment_objects.append(Equipment(total_value=equipment_data.get("total_value")))
    return _calculate_total_cost(insurance, equipment_objects)


@transaction.atomic
def equipment_insurance_create(
    *,
    nature: str,
    equipment: list,
    postcode_city: PostcodeCity = None,
    country: str = None,
    **base_insurance_fields,
) -> EquipmentInsurance:
    type = InsuranceType.objects.equipment()
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(**base_insurance_fields, type=type)
    insurance = EquipmentInsurance(
        nature=nature,
        postcode=int(postcode_city.postcode) if postcode_city else None,
        city=postcode_city.name if postcode_city else None,
        **base_insurance_fields,
    )
    insurance.country = country
    # We can only calculate after equipments added so for now add 0
    insurance.total_cost = 0
    insurance.full_clean()
    insurance.save()

    # Save insurance here already so we can create equipment linked to it
    # This whole function is atomic so if equipment cant be created this will rollback aswell
    for equipment_data in equipment:
        equipment = EquipmentService.equipment_create(**equipment_data, insurance=insurance)
    insurance.total_cost = _calculate_total_cost(insurance)
    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def equipment_insurance_delete(*, insurance: EquipmentInsurance):
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.equipment.clear()
    insurance.delete()


@transaction.atomic
def equipment_insurance_update(*, insurance: EquipmentInsurance, **fields) -> EquipmentInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    equipment_insurance_delete(insurance=insurance)
    new_insurance = equipment_insurance_create(**fields, id=old_id)
    return new_insurance
