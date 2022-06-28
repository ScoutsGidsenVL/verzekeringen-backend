from decimal import Decimal

from django.db import transaction

from scouts_insurances.insurances.models import ActivityInsurance, InsuranceType, CostVariable
from scouts_insurances.insurances.models.enums import GroupSize
from scouts_insurances.insurances.services import BaseInsuranceService


class ActivityInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: ActivityInsurance) -> Decimal:
        premium = CostVariable.objects.get_variable(insurance.type, "premium")
        cost = round(insurance.group_size.value * premium.value, 2)

        return cost

    # We create an insurance in memory (! so no saving) and calculate cost
    def activity_insurance_cost_calculation(
        self, *, nature: str, group_size: GroupSize, postal_code: int, city: str, **base_insurance_fields
    ) -> Decimal:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.activity()
        )
        insurance = ActivityInsurance(
            nature=nature,
            group_size=GroupSize(group_size),
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        return self._calculate_total_cost(insurance)

    @transaction.atomic
    def activity_insurance_create(
        self, *, nature: str, group_size: GroupSize, postal_code: int, city: str, **base_insurance_fields
    ) -> ActivityInsurance:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.activity()
        )
        insurance = ActivityInsurance(
            nature=nature,
            group_size=GroupSize(group_size),
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance, base_insurance_fields.get("responsible_member"))

        return insurance

    @transaction.atomic
    def activity_insurance_delete(self, *, insurance: ActivityInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.delete()

    @transaction.atomic
    def activity_insurance_update(self, *, insurance: ActivityInsurance, **fields) -> ActivityInsurance:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.activity_insurance_delete(insurance=insurance)
        new_insurance = self.activity_insurance_create(**fields, id=old_id)
        return new_insurance
