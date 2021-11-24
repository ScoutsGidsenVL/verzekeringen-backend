import logging
from decimal import Decimal

from django.db import transaction
from django.db.models import Q

from apps.equipment.services import EquipmentService
from apps.equipment.models import Equipment, EquipmentInuitsTemplate
from apps.insurances.models import EquipmentInsurance, InsuranceType, CostVariable
from apps.insurances.models.enums import InsuranceStatus
from apps.insurances.services import BaseInsuranceService

from groupadmin.models import PostcodeCity


logger = logging.getLogger(__name__)


class EquipmentInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: EquipmentInsurance, equipment_list: list = []) -> Decimal:
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
        self,
        *,
        nature: str,
        equipment: list,
        postcode_city: PostcodeCity = None,
        country: str = None,
        **base_insurance_fields,
    ) -> Decimal:
        type = InsuranceType.objects.equipment()
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
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
        return self._calculate_total_cost(insurance, equipment_objects)

    @transaction.atomic
    def equipment_insurance_create(
        self,
        *,
        nature: str,
        equipment: list,
        postcode_city: PostcodeCity = None,
        country: str = None,
        **base_insurance_fields,
    ) -> EquipmentInsurance:
        type = InsuranceType.objects.equipment()
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
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
        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def equipment_insurance_delete(self, *, insurance: EquipmentInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.equipment.clear()
        insurance.delete()

    @transaction.atomic
    def equipment_insurance_update(self, *, insurance: EquipmentInsurance, **fields) -> EquipmentInsurance:
        # The equipment list contains instances that are already persisted in InuitsEquipment
        # No need to update the InuitsEquipment instances.
        insurance.start_date = fields.get("start_date", insurance.start_date)
        insurance.end_date = fields.get("end_date", insurance.end_date)
        insurance.nature = fields.get("nature", insurance.nature)
        insurance.postcode = fields.get("postcode_city.postcode", insurance.postcode)
        insurance.city = fields.get("postcode_city.city", insurance.city)

        insurance.full_clean()
        insurance.save()

        # If a piece of equipment was removed from the list, also remove it from the database.
        # Make sure the equipment is not part of an insurance request that is not new or waiting (i.e. already approved or billed).
        existing_equipment_list = [
            equipment.id
            for equipment in Equipment.objects.filter(
                Q(insurance=insurance)
                | Q(insurance__insurance_parent___status__in=[InsuranceStatus.NEW, InsuranceStatus.WAITING])
            )
        ]

        for equipment_data in fields.get("equipment", []):
            equipment_id = equipment_data.get("id", None)
            inuits_equipment_id = equipment_data.get("inuits_equipment_id", None)

            equipment = EquipmentService.equipment_create_or_update(**equipment_data, insurance=insurance)

            if equipment_id and equipment_id in existing_equipment_list:
                existing_equipment_list.remove(equipment.id)

        for equipment_id in existing_equipment_list:
            logger.debug("Deleting unused equipment %s from insurance %s", equipment_id, insurance.id)
            equipment = Equipment.objects.get(pk=equipment_id)

            EquipmentInuitsTemplate.objects.get(equipment=equipment).delete()
            equipment.delete()

        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()
