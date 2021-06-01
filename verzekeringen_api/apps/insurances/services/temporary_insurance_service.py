from django.db import transaction
from apps.members.utils import PostcodeCity
from apps.members.models import InuitsNonMember
from ..models import TemporaryInsurance, InsuranceType
from . import base_insurance_service as BaseInsuranceService


@transaction.atomic
def temporary_insurance_create(
    *,
    nature: str,
    non_members: list[InuitsNonMember],
    country: str = None,
    location: PostcodeCity = None,
    **base_insurance_fields,
) -> TemporaryInsurance:
    # TODO calculate cost
    total_cost = 1
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, total_cost=total_cost, type=InsuranceType.objects.temporary()
    )
    insurance = TemporaryInsurance(
        nature=nature,
        country=country,
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def temporary_insurance_update(*, insurance: TemporaryInsurance, **fields) -> TemporaryInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.delete()
    new_insurance = activity_insurance_create(**fields, id=old_id)
    return new_insurance
