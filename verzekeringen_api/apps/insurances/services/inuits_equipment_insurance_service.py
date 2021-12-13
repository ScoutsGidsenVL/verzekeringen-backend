from django.db import transaction

from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.services import EquipmentInsuranceService


class InuitsEquipmentInsuranceService(EquipmentInsuranceService):
    @transaction.atomic
    def equipment_insurance_create(
        self,
        *args,
        nature: str,
        equipment: list,
        postal_code: int = None,
        city: str = None,
        country: str = None,
        **base_insurance_fields,
    ) -> EquipmentInsurance:
        insurance = super().equipment_insurance_create(
            nature=nature,
            equipment=equipment,
            postal_code=postal_code,
            city=city,
            country=country,
            **base_insurance_fields,
        )

        return insurance
