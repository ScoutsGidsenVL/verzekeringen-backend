from django.db import transaction
from decimal import Decimal
from apps.locations.utils import PostcodeCity
from apps.members.services import MemberService
from ..models import TemporaryInsurance, InsuranceType, CostVariable
from . import base_insurance_service as BaseInsuranceService


def _calculate_total_cost(insurance: TemporaryInsurance, non_member_amount: int) -> Decimal:
    premium = CostVariable.objects.get_variable(insurance.type, "premium")
    cost = round(non_member_amount * premium.value, 2)

    return cost


# We create an insurance in memory (! so no saving) and calculate cost
def temporary_insurance_cost_calculation(
    *,
    nature: str,
    non_members: list[dict],
    country: str = None,
    postcode_city: PostcodeCity = None,
    **base_insurance_fields,
) -> Decimal:
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, type=InsuranceType.objects.temporary()
    )
    insurance = TemporaryInsurance(
        nature=nature,
        postcode=int(postcode_city.postcode) if postcode_city else None,
        city=postcode_city.name if postcode_city else None,
        **base_insurance_fields,
    )
    insurance.country = country

    return _calculate_total_cost(insurance, len(non_members))


@transaction.atomic
def temporary_insurance_create(
    *,
    nature: str,
    non_members: list[dict],
    country: str = None,
    postcode_city: PostcodeCity = None,
    **base_insurance_fields,
) -> TemporaryInsurance:
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, type=InsuranceType.objects.temporary()
    )
    insurance = TemporaryInsurance(
        nature=nature,
        postcode=int(postcode_city.postcode) if postcode_city else None,
        city=postcode_city.name if postcode_city else None,
        **base_insurance_fields,
    )
    insurance.country = country
    insurance.total_cost = _calculate_total_cost(insurance, len(non_members))
    insurance.full_clean()
    insurance.save()

    # Save insurance here already so we can create non members linked to it
    # This whole function is atomic so if non members cant be created this will rollback aswell
    for non_member_data in non_members:
        non_member = MemberService.non_member_create(**non_member_data)
        insurance.non_members.add(non_member)

    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def temporary_insurance_delete(*, insurance: TemporaryInsurance):
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.non_members.clear()
    insurance.delete()


@transaction.atomic
def temporary_insurance_update(*, insurance: TemporaryInsurance, **fields) -> TemporaryInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    temporary_insurance_delete(insurance=insurance)
    new_insurance = temporary_insurance_create(**fields, id=old_id)
    return new_insurance
