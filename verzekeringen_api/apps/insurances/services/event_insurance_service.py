from decimal import Decimal

from django.db import transaction

from apps.insurances.models import EventInsurance, InsuranceType, CostVariable
from apps.insurances.services import BaseInsuranceService

from groupadmin.models import PostcodeCity


class EventInsuranceService:
    base_insurance_service = BaseInsuranceService()

    def _calculate_total_cost(self, insurance: EventInsurance) -> Decimal:
        days = (insurance.end_date - insurance.start_date).days
        if days == 0:
            days = 1

        premium = CostVariable.objects.get_variable(insurance.type, "premium_%s" % str(insurance.event_size)).value
        cost = round(days * premium, 2)

        return cost

    # We create an insurance in memory (! so no saving) and calculate cost
    def event_insurance_cost_calculation(
        self, *, nature: str, event_size: int, location: PostcodeCity, **base_insurance_fields
    ) -> Decimal:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.event()
        )
        insurance = EventInsurance(
            nature=nature,
            event_size=event_size,
            postcode=int(location.postcode),
            city=location.name,
            **base_insurance_fields,
        )
        return self._calculate_total_cost(insurance)

    @transaction.atomic
    def event_insurance_create(
        self, *, nature: str, event_size: int, location: PostcodeCity, **base_insurance_fields
    ) -> EventInsurance:
        base_insurance_fields = self.base_insurance_service.base_insurance_creation_fields(
            **base_insurance_fields, type=InsuranceType.objects.event()
        )
        insurance = EventInsurance(
            nature=nature,
            event_size=event_size,
            postcode=int(location.postcode),
            city=location.name,
            **base_insurance_fields,
        )
        insurance.total_cost = self._calculate_total_cost(insurance)
        insurance.full_clean()
        insurance.save()

        self.base_insurance_service.handle_insurance_created(insurance)

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
