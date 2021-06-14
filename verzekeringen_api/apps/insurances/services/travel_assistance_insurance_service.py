import math
from django.db import transaction
from decimal import Decimal
from apps.equipment.utils import Vehicle
from apps.members.services import MemberService
from ..models import TravelAssistanceInsurance, InsuranceType, CostVariable
from . import base_insurance_service as BaseInsuranceService


def _cost_by_prefix(prefix: str, type: InsuranceType, active_limit: int, days: int) -> Decimal:
    if not active_limit:
        # If no active limit we need to get price of max so 32 and calculate extra months
        cost = CostVariable.objects.get_variable(type, "%s_32" % (prefix)).value
        monthly_cost = CostVariable.objects.get_variable(type, "%s_extramonth" % (prefix)).value
        extra_months = math.ceil((days - 32) / 30)
        cost += extra_months * monthly_cost
    else:
        cost = CostVariable.objects.get_variable(type, "%s_%s" % (prefix, str(active_limit))).value
    return cost


def _calculate_total_cost(insurance: TravelAssistanceInsurance, participant_amount: int) -> Decimal:
    days = (insurance.end_date - insurance.start_date).days
    limits = (1, 3, 5, 11, 17, 23, 32)

    active_limit = None
    for limit in limits:
        if days <= limit:
            active_limit = limit
            break

    if insurance.vehicle:
        cost = participant_amount * _cost_by_prefix("premium_participant", insurance.type, active_limit, days)
        cost += _cost_by_prefix("premium_vehicle", insurance.type, active_limit, days)
    else:
        # TODO seperate european and world
        cost = participant_amount * _cost_by_prefix("premium_europe", insurance.type, active_limit, days)

    return round(cost, 2)


# We create an insurance in memory (! so no saving) and calculate cost
def travel_assistance_insurance_cost_calculation(
    *,
    participants: list,
    country: str,
    vehicle: Vehicle = None,
    **base_insurance_fields,
) -> Decimal:
    type = (
        InsuranceType.objects.travel_assistance_without_vehicle()
        if vehicle is None
        else InsuranceType.objects.travel_assistance_with_vehicle()
    )
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(**base_insurance_fields, type=type)
    insurance = TravelAssistanceInsurance(
        country=country,
        **base_insurance_fields,
    )
    if vehicle:
        insurance.vehicle = vehicle
    return _calculate_total_cost(insurance, len(participants))


@transaction.atomic
def travel_assistance_insurance_create(
    *,
    participants: list,
    country: str,
    vehicle: Vehicle = None,
    **base_insurance_fields,
) -> TravelAssistanceInsurance:
    type = (
        InsuranceType.objects.travel_assistance_without_vehicle()
        if vehicle is None
        else InsuranceType.objects.travel_assistance_with_vehicle()
    )
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(**base_insurance_fields, type=type)
    insurance = TravelAssistanceInsurance(
        country=country,
        **base_insurance_fields,
    )
    if vehicle:
        insurance.vehicle = vehicle
    insurance.total_cost = _calculate_total_cost(insurance, len(participants))
    insurance.full_clean()
    insurance.save()

    # Save insurance here already so we can create non members linked to it
    # This whole function is atomic so if non members cant be created this will rollback aswell
    for participant_data in participants:
        participant = MemberService.non_member_create(**participant_data)
        insurance.participants.add(participant)

    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def travel_assistance_insurance_delete(*, insurance: TravelAssistanceInsurance):
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.participants.clear()
    insurance.delete()


@transaction.atomic
def travel_assistance_insurance_update(*, insurance: TravelAssistanceInsurance, **fields) -> TravelAssistanceInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    travel_assistance_insurance_delete(insurance=insurance)
    new_insurance = travel_assistance_insurance_create(**fields, id=old_id)
    return new_insurance
