from decimal import Decimal

from django.db import transaction
from django.conf import settings

from scouts_insurances.people.services import MemberService
from scouts_insurances.equipment.models import Vehicle
from scouts_insurances.insurances.models import (
    TemporaryVehicleInsurance,
    InsuranceType,
    ParticipantTemporaryVehicleInsurance,
    CostVariable,
)
from scouts_insurances.insurances.models.enums import (
    TemporaryVehicleParticipantType,
    TemporaryVehicleInsuranceOptionApi,
)
from scouts_insurances.insurances.services import BaseInsuranceService


class TemporaryVehicleInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: TemporaryVehicleInsurance) -> Decimal:
        days = (insurance.end_date - insurance.start_date).days

        cost = 0

        if TemporaryVehicleInsuranceOptionApi.OMNIUM in insurance.insurance_options:
            limits = (8, 15, 25, 31)
            for limit in limits:
                if days <= limit:
                    cost += CostVariable.objects.get_variable(insurance.type, "premium_option1_%s" % str(limit)).value
                    break

        if TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM in insurance.insurance_options:
            limits = (15, 31)
            for limit in limits:
                if days <= limit:
                    cost += CostVariable.objects.get_variable(
                        insurance.type, "premium_option2%s_%s" % (insurance.max_coverage, str(limit))
                    ).value
                    break

        if TemporaryVehicleInsuranceOptionApi.RENTAL in insurance.insurance_options:
            limits = (15, 20, 31)
            for limit in limits:
                if days <= limit:
                    cost += CostVariable.objects.get_variable(insurance.type, "premium_option3_%s" % str(limit)).value
                    break

        # Will round here because we also do that in old code and might make a difference
        cost = round(cost, 2)

        # Double if you have heavy trailer
        if insurance.vehicle.has_heavy_trailer:
            cost *= 2

        return cost

    # We create an insurance in memory (! so no saving) and calculate cost
    def temporary_vehicle_insurance_cost_calculation(
        self,
        *,
        owner: dict,
        drivers: list,
        vehicle: Vehicle,
        insurance_options: set = None,
        max_coverage: str = None,
        **base_insurance_fields,
    ) -> Decimal:
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
        return self._calculate_total_cost(insurance)

    @transaction.atomic
    def temporary_vehicle_insurance_create(
        self,
        *,
        owner: dict,
        drivers: list,
        vehicle: Vehicle,
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

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def temporary_vehicle_insurance_delete(self, *, insurance: TemporaryVehicleInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.participants.clear()
        insurance.delete()

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
