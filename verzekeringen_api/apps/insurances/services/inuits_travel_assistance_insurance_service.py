import logging

from django.db import transaction

from apps.people.services import InuitsNonMemberService

from scouts_insurances.equipment.models import TravelAssistanceVehicle
from scouts_insurances.insurances.models import TravelAssistanceInsurance, InsuranceType
from scouts_insurances.insurances.services import TravelAssistanceInsuranceService


logger = logging.getLogger(__name__)


class InuitsTravelAssistanceInsuranceService(TravelAssistanceInsuranceService):
    non_member_service = InuitsNonMemberService()

    def travel_assistance_insurance_create(
        self,
        *,
        participants: list,
        country: str,
        vehicle: TravelAssistanceVehicle = None,
        **base_insurance_fields,
    ) -> TravelAssistanceInsurance:
        type = (
            InsuranceType.objects.travel_assistance_without_vehicle()
            if vehicle is None
            else InsuranceType.objects.travel_assistance_with_vehicle()
        )
        group_admin_id = base_insurance_fields.pop("group_admin_id", None)
        if group_admin_id and not base_insurance_fields.get("scouts_group", None):
            base_insurance_fields["scouts_group"] = self.groupadmin.get_group(
                active_user=base_insurance_fields.get("created_by"), group_group_admin_id=group_admin_id
            )

        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
        insurance = TravelAssistanceInsurance(
            country=country,
            **base_insurance_fields,
        )
        if vehicle:
            insurance.vehicle = vehicle
        else:
            insurance.vehicle = None
        insurance.total_cost = self._calculate_total_cost(insurance, len(participants))
        insurance.full_clean()
        insurance.save()

        # Save insurance here already so we can create non members linked to it
        # This whole function is atomic so if non members cant be created this will rollback aswell
        for participant in participants:
            participant = self.non_member_service.non_member_create(participant)
            insurance.participants.add(participant)

        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def travel_assistance_insurance_update(
        self, *, insurance: TravelAssistanceInsurance, **fields
    ) -> TravelAssistanceInsurance:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.travel_assistance_insurance_delete(insurance=insurance)
        new_insurance = self.travel_assistance_insurance_create(**fields, id=old_id)
        return new_insurance
