from django.db import transaction
from apps.members.utils import PostcodeCity
from ..models import ActivityInsurance, InsuranceType
from ..models.enums import GroupSize
from . import base_insurance_service as BaseInsuranceService


@transaction.atomic
def activity_insurance_create(
    *, nature: str, group_size: GroupSize, location: PostcodeCity, **base_insurance_fields
) -> ActivityInsurance:
    # TODO calculate cost
    total_cost = 1
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, total_cost=total_cost, type=InsuranceType.objects.activity()
    )
    insurance = ActivityInsurance(
        nature=nature,
        group_size=GroupSize(group_size),
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
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
