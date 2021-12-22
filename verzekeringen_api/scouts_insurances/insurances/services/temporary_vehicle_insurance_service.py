import logging
from decimal import Decimal

from django.db import transaction

from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicle
from scouts_insurances.insurances.models import (
    TemporaryVehicleInsurance,
    InsuranceType,
    CostVariable,
)
from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOption
from scouts_insurances.insurances.services import BaseInsuranceService


logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: TemporaryVehicleInsurance) -> Decimal:
        days = (insurance.end_date - insurance.start_date).days

        cost = 0

        insurance_options = list(map(int, list(str(insurance.insurance_options))))

        if TemporaryVehicleInsuranceOption.OMNIUM in insurance_options:
            limits = (8, 15, 25, 31)
            for limit in limits:
                if days <= limit:
                    cost += CostVariable.objects.get_variable(insurance.type, "premium_option1_%s" % str(limit)).value
                    break

        if TemporaryVehicleInsuranceOption.COVER_OMNIUM in insurance_options:
            limits = (15, 31)
            for limit in limits:
                if days <= limit:
                    cost += CostVariable.objects.get_variable(
                        insurance.type, "premium_option2%s_%s" % (insurance.max_coverage, str(limit))
                    ).value
                    break

        if TemporaryVehicleInsuranceOption.RENTAL in insurance_options:
            limits = (15, 20, 31)
            for limit in limits:
                if days <= limit:
                    cost += CostVariable.objects.get_variable(insurance.type, "premium_option3_%s" % str(limit)).value
                    break

        # Will round here because we also do that in old code and might make a difference
        cost = round(cost, 2)

        # Double if you have heavy trailer
        if insurance.has_heavy_trailer:
            cost *= 2

        return cost

    # We create an insurance in memory (! so no saving) and calculate cost
    def temporary_vehicle_insurance_cost_calculation(
        self,
        *,
        owner: dict,
        drivers: list,
        vehicle: TemporaryVehicleInsuranceVehicle,
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
    def temporary_vehicle_insurance_delete(self, *, insurance: TemporaryVehicleInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.participants.clear()
        insurance.delete()
