from django.db import transaction
from decimal import Decimal
from apps.locations.utils import PostcodeCity
from ..models import ActivityInsurance, InsuranceType, CostVariable
from ..models.enums import GroupSize
from . import base_insurance_service as BaseInsuranceService


def _calculate_total_cost(insurance: ActivityInsurance) -> Decimal:
    premium = CostVariable.objects.get_variable(insurance.type, "premium")
    cost = round(insurance.group_size.value * premium.value, 2)

    return cost


# We create an insurance in memory (! so no saving) and calculate cost
def activity_insurance_cost_calculation(
    *, nature: str, group_size: GroupSize, location: PostcodeCity, **base_insurance_fields
) -> Decimal:
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, type=InsuranceType.objects.activity()
    )
    insurance = ActivityInsurance(
        nature=nature,
        group_size=GroupSize(group_size),
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
    return _calculate_total_cost(insurance)


@transaction.atomic
def activity_insurance_create(
    *, nature: str, group_size: GroupSize, location: PostcodeCity, **base_insurance_fields
) -> ActivityInsurance:
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, type=InsuranceType.objects.activity()
    )
    insurance = ActivityInsurance(
        nature=nature,
        group_size=GroupSize(group_size),
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
    insurance.total_cost = _calculate_total_cost(insurance)
    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def activity_insurance_delete(*, insurance: ActivityInsurance):
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.delete()


@transaction.atomic
def activity_insurance_update(*, insurance: ActivityInsurance, **fields) -> ActivityInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    activity_insurance_delete(insurance=insurance)
    new_insurance = activity_insurance_create(**fields, id=old_id)
    return new_insurance
