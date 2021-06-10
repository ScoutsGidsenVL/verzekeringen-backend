from django.db import transaction
from decimal import Decimal
from apps.locations.utils import PostcodeCity
from ..models import EventInsurance, InsuranceType, CostVariable
from ..models.enums import EventSize
from . import base_insurance_service as BaseInsuranceService


def _calculate_total_cost(insurance: EventInsurance) -> Decimal:
    days = (insurance.end_date - insurance.start_date).days

    premium = CostVariable.objects.get_variable(insurance.type, "premium_%s" % str(insurance.event_size)).value
    cost = round(days * premium, 2)

    return cost


# We create an insurance in memory (! so no saving) and calculate cost
def event_insurance_cost_calculation(
    *, nature: str, event_size: int, location: PostcodeCity, **base_insurance_fields
) -> Decimal:
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, type=InsuranceType.objects.event()
    )
    insurance = EventInsurance(
        nature=nature,
        event_size=event_size,
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
    return _calculate_total_cost(insurance)


@transaction.atomic
def event_insurance_create(
    *, nature: str, event_size: int, location: PostcodeCity, **base_insurance_fields
) -> EventInsurance:
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, type=InsuranceType.objects.event()
    )
    insurance = EventInsurance(
        nature=nature,
        event_size=event_size,
        postcode=int(location.postcode),
        city=location.name,
        **base_insurance_fields,
    )
    insurance.total_cost = _calculate_total_cost(insurance)
    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def event_insurance_delete(*, insurance: EventInsurance):
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.delete()


@transaction.atomic
def event_insurance_update(*, insurance: EventInsurance, **fields) -> EventInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    event_insurance_delete(insurance=insurance)
    new_insurance = event_insurance_create(**fields, id=old_id)
    return new_insurance
