import logging, math
from decimal import Decimal

from django.db import transaction

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.services import BaseInsuranceService

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class TravelAssistanceInsuranceService:
    base_insurance_service = BaseInsuranceService()
    groupadmin = GroupAdmin()

    def calculate_total_cost(self, days_amount:int, person_amount:int=0, vehicle_amount:int=0) -> Decimal:
        """
        Calculates the cost of a insurance based on the given params.

        Policy description: Ethias assistance - Travel abroad
        Policy price calculation:
         - Per person worldwide coverage: 1.00 EUR/day
         - Per vehicle in europe coverage: 2.50 EUR/day
         - Minimum yearly premium: 100.00 EUR
         - Tax 9.25%
         - RIZIV 7.5% (only for vehicle coverage)
        """
        cost = Decimal(0.0)
        if person_amount:
            cost += days_amount * Decimal(1.0) * person_amount * (
                1 + Decimal(0.0925))
        if vehicle_amount:
            cost += days_amount * Decimal(2.5) * vehicle_amount * (
                1 + Decimal(0.0925) + Decimal(0.075))
        return cost

    @transaction.atomic
    def travel_assistance_insurance_delete(self, *, insurance: TravelAssistanceInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.participants.clear()
        insurance.delete()
