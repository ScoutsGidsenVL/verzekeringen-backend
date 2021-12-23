import logging
from typing import List

from django.db import transaction

from apps.people.models import InuitsNonMember
from apps.people.services import InuitsNonMemberService

from scouts_insurances.insurances.models import TemporaryInsurance, InsuranceType
from scouts_insurances.insurances.services import TemporaryInsuranceService


logger = logging.getLogger(__name__)


class InuitsTemporaryInsuranceService(TemporaryInsuranceService):
    non_member_service = InuitsNonMemberService()

    @transaction.atomic
    def inuits_temporary_insurance_create(
        self,
        *,
        nature: str,
        non_members: List[InuitsNonMember] = [],
        country: str = None,
        postal_code: int = None,
        city: str = None,
        **base_insurance_fields,
    ) -> TemporaryInsurance:
        logger.debug("NON-MEMBERS: %s", non_members)
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
        for non_member in non_members:
            non_member = self.non_member_service.linked_non_member_create(
                inuits_non_member=non_member, created_by=base_insurance_fields.get("created_by")
            )
            insurance.non_members.add(non_member)

        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def temporary_insurance_update(self, *, insurance: TemporaryInsurance, **fields) -> TemporaryInsurance:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.temporary_insurance_delete(insurance=insurance)
        new_insurance = self.inuits_temporary_insurance_create(**fields, id=old_id)
        return new_insurance
