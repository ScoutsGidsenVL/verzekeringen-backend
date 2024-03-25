import logging

from django.conf import settings
from django.db import transaction

from apps.people.services import InuitsNonMemberService
from scouts_insurances.equipment.models import TravelAssistanceVehicle
from scouts_insurances.insurances.models import InsuranceType, TravelAssistanceInsurance
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
        # @TODO: should be fixed in the frontend: either group_admin_id or group_group_admin_id, not both
        group_admin_id = base_insurance_fields.pop(
            "group_admin_id", base_insurance_fields.pop("group_group_admin_id", None)
        )
        scouts_group = base_insurance_fields.pop("scouts_group", None)
        if group_admin_id and not scouts_group:
            scouts_group = self.groupadmin.get_group(
                active_user=base_insurance_fields.get("created_by"), group_group_admin_id=group_admin_id
            )

        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            scouts_group=scouts_group, **base_insurance_fields, type=type
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

        # result = Country.objects.by_insurance_type_id(insurance.country.name)
        if insurance.country:
            insurance.country = insurance.country.name

        insurance.full_clean()
        insurance.save()

        # Save insurance here already so we can create non members linked to it
        # This whole function is atomic so if non members cant be created this will rollback aswell
        for participant in participants:
            participant = self.non_member_service.linked_non_member_create(
                inuits_non_member=participant, created_by=base_insurance_fields.get("created_by")
            )

            insurance.participants.add(participant)

        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(
            insurance, created_by=base_insurance_fields.get("responsible_member")
        )

        return insurance

    @transaction.atomic
    def travel_assistance_insurance_update(
        self, *, insurance: TravelAssistanceInsurance, created_by: settings.AUTH_USER_MODEL, **fields
    ) -> TravelAssistanceInsurance:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.travel_assistance_insurance_delete(insurance=insurance)
        new_insurance = self.travel_assistance_insurance_create(**fields, id=old_id, created_by=created_by)
        return new_insurance
