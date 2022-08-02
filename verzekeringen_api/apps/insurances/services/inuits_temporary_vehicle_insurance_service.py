import logging
from typing import List

from django.db import transaction
from django.conf import settings

from apps.people.models import InuitsNonMember
from apps.people.services import InuitsNonMemberService

from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicle
from scouts_insurances.insurances.models import (
    TemporaryVehicleInsurance,
    InsuranceType,
    ParticipantTemporaryVehicleInsurance,
)
from scouts_insurances.insurances.models.enums import TemporaryVehicleParticipantType
from scouts_insurances.insurances.services import TemporaryVehicleInsuranceService


logger = logging.getLogger(__name__)


class InuitsTemporaryVehicleInsuranceService(TemporaryVehicleInsuranceService):
    non_member_service = InuitsNonMemberService()

    @transaction.atomic
    def temporary_vehicle_insurance_create(
        self,
        *,
        owner: InuitsNonMember,
        drivers: List[InuitsNonMember],
        vehicle: TemporaryVehicleInsuranceVehicle,
        insurance_options: set = None,
        max_coverage: str = None,
        **base_insurance_fields,
    ) -> TemporaryVehicleInsurance:

        type = InsuranceType.objects.temporary_vehicle()
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
        insurance = TemporaryVehicleInsurance(
            max_coverage=max_coverage,
            **base_insurance_fields,
        )
        insurance.insurance_options = insurance_options
        insurance.vehicle = vehicle
        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()

        # if vehicle.inuits_vehicle_id:
        #     inuits_vehicle = InuitsVehicle.objects.filter(id=vehicle.inuits_vehicle_id).first()
        #     if inuits_vehicle:
        #         VehicleInuitsTemplate(temporary_vehicle_insurance=insurance, inuits_vehicle=inuits_vehicle).save()

        # Save insurance here already so we can create non members linked to it
        # This whole function is atomic so if non members cant be created this will rollback aswell

        for driver in drivers:
            driver = self.non_member_service.linked_non_member_create(
                inuits_non_member=driver, created_by=base_insurance_fields.get("created_by")
            )
            driver_insurance = ParticipantTemporaryVehicleInsurance(
                participant=driver, insurance=insurance, type=TemporaryVehicleParticipantType.DRIVER
            )

            driver_insurance.full_clean()
            driver_insurance.save()
       

        # Check if owner is a company and change fields to non member
        # if owner.get("company_name"):
        #     owner["first_name"] = settings.COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME
        #     owner["last_name"] = owner.get("company_name")
        #     owner.pop("company_name")
        if owner.company_name:
            owner.first_name = settings.COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME
            owner.last_name = owner.company_name


        owner = self.non_member_service.linked_non_member_create(
            inuits_non_member=owner, created_by=base_insurance_fields.get("created_by")
        )

        owner_insurance = ParticipantTemporaryVehicleInsurance(
            participant=owner, insurance=insurance, type=TemporaryVehicleParticipantType.OWNER
        )
        owner_insurance.full_clean()
        owner_insurance.save()

        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance, created_by=base_insurance_fields.get("responsible_member"))

        return insurance

    @transaction.atomic
    def temporary_vehicle_insurance_update(
        self, *, insurance: TemporaryVehicleInsurance, **fields
    ) -> TemporaryVehicleInsurance:


        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.temporary_vehicle_insurance_delete(insurance=insurance)
        new_insurance = self.temporary_vehicle_insurance_create(**fields, id=old_id)
        return new_insurance
