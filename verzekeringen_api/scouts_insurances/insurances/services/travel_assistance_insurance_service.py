import math
from decimal import Decimal

from django.db import transaction

from scouts_insurances.people.services import MemberService
from scouts_insurances.equipment.models import Vehicle
from scouts_insurances.locations.models import Country
from scouts_insurances.insurances.models import TravelAssistanceInsurance, InsuranceType, CostVariable
from scouts_insurances.insurances.services import BaseInsuranceService

from scouts_auth.groupadmin.services import GroupAdmin


class TravelAssistanceInsuranceService:
    base_insurance_service = BaseInsuranceService()
    groupadmin = GroupAdmin()
    member_service = MemberService()

    def _cost_by_prefix(self, prefix: str, type: InsuranceType, active_limit: int, days: int) -> Decimal:
        if not active_limit:
            # If no active limit we need to get price of max so 32 and calculate extra months
            cost = CostVariable.objects.get_variable(type, "%s_32" % (prefix)).value
            monthly_cost = CostVariable.objects.get_variable(type, "%s_extramonth" % (prefix)).value
            extra_months = math.ceil((days - 32) / 30)
            cost += extra_months * monthly_cost
        else:
            cost = CostVariable.objects.get_variable(type, "%s_%s" % (prefix, str(active_limit))).value
        return cost

    def _calculate_total_cost(self, insurance: TravelAssistanceInsurance, participant_amount: int) -> Decimal:
        days = (insurance.end_date - insurance.start_date).days
        limits = (1, 3, 5, 11, 17, 23, 32)

        active_limit = None
        for limit in limits:
            if days <= limit:
                active_limit = limit
                break

        if insurance.vehicle:
            cost = participant_amount * self._cost_by_prefix("premium_participant", insurance.type, active_limit, days)
            cost += self._cost_by_prefix("premium_vehicle", insurance.type, active_limit, days)
        else:
            # TODO seperate european and world
            cost = participant_amount * self._cost_by_prefix("premium_europe", insurance.type, active_limit, days)

        return round(cost, 2)

    # We create an insurance in memory (! so no saving) and calculate cost
    def travel_assistance_insurance_cost_calculation(
        self,
        *,
        participants: list,
        country: str = None,
        vehicle: Vehicle = None,
        group_admin_id: str = "",
        **base_insurance_fields,
    ) -> Decimal:
        type = (
            InsuranceType.objects.travel_assistance_without_vehicle()
            if vehicle is None
            else InsuranceType.objects.travel_assistance_with_vehicle()
        )
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=type
        )
        country = country if country and isinstance(country, str) else Country.DEFAULT_COUNTRY_NAME
        insurance = TravelAssistanceInsurance(
            **base_insurance_fields,
        )
        insurance.country = country
        if vehicle:
            insurance.vehicle = vehicle
        return self._calculate_total_cost(insurance, len(participants))

    @transaction.atomic
    def travel_assistance_insurance_create(
        self,
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
        for participant_data in participants:
            participant = self.member_service.non_member_create(**participant_data)
            insurance.participants.add(participant)

        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance)

        return insurance

    @transaction.atomic
    def travel_assistance_insurance_delete(self, *, insurance: TravelAssistanceInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.participants.clear()
        insurance.delete()

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
