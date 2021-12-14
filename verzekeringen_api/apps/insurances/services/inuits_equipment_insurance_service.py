from django.db import transaction

from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.services import EquipmentInsuranceService


class InuitsEquipmentInsuranceService(EquipmentInsuranceService):
    @transaction.atomic
    def equipment_insurance_create(
        self,
        *args,
        **base_insurance_fields,
    ) -> EquipmentInsurance:
        insurance = super().equipment_insurance_create(
            *args,
            **base_insurance_fields,
        )

        return insurance
