from django.db import transaction
from apps.members.utils import PostcodeCity
from ..models import ActivityInsurance, InsuranceType
from . import base_insurance_service as BaseInsuranceService


@transaction.atomic
def activity_insurance_create(
    *, nature: str, group_amount: int, location: PostcodeCity, **base_insurance_fields
) -> ActivityInsurance:
    # TODO calculate cost
    total_cost = 1
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, total_cost=total_cost, type=InsuranceType.objects.activity()
    )
    insurance = ActivityInsurance(
        nature=nature,
        group_amount=group_amount,
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
    insurance.full_clean()
    insurance.save()

    return insurance
