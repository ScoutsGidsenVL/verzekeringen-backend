import logging, math
from decimal import Decimal

from django.db import transaction

from scouts_insurances.equipment.models import TravelAssistanceVehicle
from scouts_insurances.locations.models import Country
from scouts_insurances.insurances.models import TravelAssistanceInsurance, InsuranceType, CostVariable
from scouts_insurances.insurances.services import BaseInsuranceService

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class TravelAssistanceInsuranceService:
    base_insurance_service = BaseInsuranceService()
    groupadmin = GroupAdmin()

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
        vehicle: TravelAssistanceVehicle = None,
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
    def travel_assistance_insurance_delete(self, *, insurance: TravelAssistanceInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.participants.clear()
        insurance.delete()
