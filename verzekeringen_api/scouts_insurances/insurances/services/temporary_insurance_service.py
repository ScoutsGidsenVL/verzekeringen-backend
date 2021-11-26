from decimal import Decimal

from django.db import transaction

from scouts_insurances.people.services import MemberService
from scouts_insurances.insurances.models import TemporaryInsurance, InsuranceType, CostVariable
from scouts_insurances.insurances.services import BaseInsuranceService


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
    def temporary_insurance_create(
        self,
        *,
        nature: str,
        non_members: list,
        country: str = None,
        postal_code: int = None,
        city: str = None,
        **base_insurance_fields,
    ) -> TemporaryInsurance:
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
        insurance.total_cost = self._calculate_total_cost(insurance, len(non_members))
        insurance.full_clean()
        insurance.save()

        # Save insurance here already so we can create non members linked to it
        # This whole function is atomic so if non members cant be created this will rollback aswell
        for non_member_data in non_members:
            non_member = MemberService.non_member_create(**non_member_data)
            insurance.non_members.add(non_member)

        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def temporary_insurance_delete(self, *, insurance: TemporaryInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.non_members.clear()
        insurance.delete()

    @transaction.atomic
    def temporary_insurance_update(self, *, insurance: TemporaryInsurance, **fields) -> TemporaryInsurance:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.temporary_insurance_delete(insurance=insurance)
        new_insurance = self.temporary_insurance_create(**fields, id=old_id)
        return new_insurance
