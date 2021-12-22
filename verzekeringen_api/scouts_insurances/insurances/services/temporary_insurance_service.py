import logging

from decimal import Decimal

from django.db import transaction

from scouts_insurances.insurances.models import TemporaryInsurance, InsuranceType, CostVariable
from scouts_insurances.insurances.services import BaseInsuranceService


logger = logging.getLogger(__name__)


class TemporaryInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: TemporaryInsurance, non_member_amount: int) -> Decimal:
        premium = CostVariable.objects.get_variable(insurance.type, "premium")
        cost = round(non_member_amount * premium.value, 2)

        return cost

    # We create an insurance in memory (! so no saving) and calculate cost
    def temporary_insurance_cost_calculation(
        self,
        *,
        nature: str,
        non_members: list,
        country: str = None,
        postal_code: int = None,
        city: str = None,
        **base_insurance_fields,
    ) -> Decimal:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.temporary()
        )
        insurance = TemporaryInsurance(
            nature=nature,
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        insurance.country = country

        return self._calculate_total_cost(insurance, len(non_members))

    @transaction.atomic
    def temporary_insurance_delete(self, *, insurance: TemporaryInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.non_members.clear()
        insurance.delete()
