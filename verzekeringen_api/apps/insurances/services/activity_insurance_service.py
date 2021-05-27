from django.db import transaction
from ..models import ActivityInsurance, InsuranceType
from . import base_insurance_service as BaseInsuranceService


@transaction.atomic
def activity_insurance_create(
    *, nature: str, group_amount: int, postcode: int, city: str, **base_insurance_fields
) -> ActivityInsurance:
    # TODO calculate cost
    total_cost = 1
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, total_cost=total_cost, type=InsuranceType.objects.activity()
    )
    insurance = ActivityInsurance(
        nature=nature,
        group_amount=group_amount,
        postcode=postcode,
        city=city,
        **base_insurance_fields,
    )
    insurance.full_clean()
    insurance.save()

    return insurance
