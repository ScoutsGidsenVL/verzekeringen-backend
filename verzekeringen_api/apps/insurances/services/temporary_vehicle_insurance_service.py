from django.db import transaction
from django.conf import settings
from apps.equipment.utils import Vehicle
from apps.members.services import MemberService
from ..models import TemporaryVehicleInsurance, InsuranceType, ParticipantTemporaryVehicleInsurance
from ..models.enums import TemporaryVehicleParticipantType
from . import base_insurance_service as BaseInsuranceService


@transaction.atomic
def temporary_vehicle_insurance_create(
    *,
    owner: dict,
    drivers: list[dict],
    vehicle: Vehicle,
    insurance_option: int = None,
    max_coverage: str = None,
    **base_insurance_fields,
) -> TemporaryVehicleInsurance:
    # TODO calculate cost
    total_cost = 1
    type = InsuranceType.objects.temporary_vehicle()
    base_insurance_fields = BaseInsuranceService.base_insurance_creation_fields(
        **base_insurance_fields, total_cost=total_cost, type=type
    )
    insurance = TemporaryVehicleInsurance(
        insurance_option=insurance_option,
        max_coverage=max_coverage,
        **base_insurance_fields,
    )
    insurance.vehicle = vehicle
    insurance.full_clean()
    insurance.save()

    # Save insurance here already so we can create non members linked to it
    # This whole function is atomic so if non members cant be created this will rollback aswell
    for driver_data in drivers:
        driver = MemberService.non_member_create(**driver_data)
        driver_insurance = ParticipantTemporaryVehicleInsurance(
            participant=driver, insurance=insurance, type=TemporaryVehicleParticipantType.DRIVER
        )
        driver_insurance.full_clean()
        driver_insurance.save()

    # Check if owner is a company and change fields to non member
    if owner.get("company_name"):
        owner["first_name"] = settings.COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME
        owner["last_name"] = owner.get("company_name")
        owner.pop("company_name")
    owner_model = MemberService.non_member_create(**owner)
    owner_insurance = ParticipantTemporaryVehicleInsurance(
        participant=owner_model, insurance=insurance, type=TemporaryVehicleParticipantType.OWNER
    )
    owner_insurance.full_clean()
    owner_insurance.save()

    insurance.full_clean()
    insurance.save()

    return insurance


@transaction.atomic
def temporary_vehicle_insurance_delete(*, insurance: TemporaryVehicleInsurance):
    insurance = BaseInsuranceService.base_insurance_delete_relations(insurance=insurance)
    insurance.participants.clear()
    insurance.delete()


@transaction.atomic
def temporary_vehicle_insurance_update(*, insurance: TemporaryVehicleInsurance, **fields) -> TemporaryVehicleInsurance:
    # For this update we just delete the old one and create a new one with the given fields (but same id)
    # Bit of a cheat but it matches expectations of customer
    old_id = insurance.id
    temporary_vehicle_insurance_delete(insurance=insurance)
    new_insurance = temporary_vehicle_insurance_create(**fields, id=old_id)
    return new_insurance
