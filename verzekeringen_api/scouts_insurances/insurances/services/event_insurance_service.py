import sys
from datetime import timedelta
from decimal import Decimal
from math import ceil

from django.db import transaction

from scouts_insurances.insurances.models import EventInsurance, InsuranceType, CostVariable
from scouts_insurances.insurances.services import BaseInsuranceService


class EventInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: EventInsurance) -> Decimal:
        days = ceil(((insurance.end_date.timestamp() - insurance.start_date.timestamp())/3600)/24)
        if days == 0:
            days = 1

        premium = CostVariable.objects.get_variable(insurance.type, "premium_%s" % str(insurance.event_size)).value
        cost = round(days * premium, 2)

        return cost

    # We create an insurance in memory (! so no saving) and calculate cost
    def event_insurance_cost_calculation(
        self, *, nature: str, event_size: int, postal_code: int, city: str, **base_insurance_fields
    ) -> Decimal:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.event()
        )
        insurance = EventInsurance(
            nature=nature,
            event_size=event_size,
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        return self._calculate_total_cost(insurance)

    @transaction.atomic
    def event_insurance_create(
        self, *, nature: str, event_size: int, postal_code: int, city: str, **base_insurance_fields
    ) -> EventInsurance:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.event()
        )
        insurance = EventInsurance(
            nature=nature,
            event_size=event_size,
            postal_code=postal_code,
            city=city,
            **base_insurance_fields,
        )
        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance, created_by=base_insurance_fields.get("responsible_member"))

        return insurance

    @transaction.atomic
    def event_insurance_delete(self, *, insurance: EventInsurance):
        insurance = self.base_insurance_service.base_insurance_delete_relations(insurance=insurance)
        insurance.delete()

    @transaction.atomic
    def event_insurance_update(self, *, insurance: EventInsurance, **fields) -> EventInsurance:
        # For this update we just delete the old one and create a new one with the given fields (but same id)
        # Bit of a cheat but it matches expectations of customer
        old_id = insurance.id
        self.event_insurance_delete(insurance=insurance)
        new_insurance = self.event_insurance_create(**fields, id=old_id)
        return new_insurance
