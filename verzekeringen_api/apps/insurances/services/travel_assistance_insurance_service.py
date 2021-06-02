from django.db import transaction
from apps.equipment.utils import Vehicle
from apps.members.services import MemberService
from ..models import TravelAssistanceInsurance, InsuranceType
from . import base_insurance_service as BaseInsuranceService


@transaction.atomic
def travel_assistance_insurance_create(
    *,
    participants: list[dict],
    country: str,
    vehicle: Vehicle = None,
    **base_insurance_fields,
) -> TravelAssistanceInsurance:
    # TODO calculate cost
    total_cost = 1
    type = (
        InsuranceType.objects.travel_assistance_without_vehicle()
        if vehicle is None
        else InsuranceType.objects.travel_assistance_with_vehicle()
    )
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, total_cost=total_cost, type=type
    )
    insurance = TravelAssistanceInsurance(
        country=country,
        **base_insurance_fields,
    )
    if vehicle:
        insurance.vehicle = vehicle
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
