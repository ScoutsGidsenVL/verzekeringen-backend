from django.db import models

from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.insurances.managers import InsuranceTypeManager


class InsuranceType(models.Model):

    objects = InsuranceTypeManager()

    id = models.IntegerField(db_column="verzekeringstypeid", primary_key=True)
    name = models.CharField(db_column="verzekeringstype", max_length=30)
    description = models.CharField(db_column="verzekeringstypeomschr", max_length=50)
    max_term = models.CharField(db_column="maxtermijn", max_length=10)

    class Meta:
        db_table = "vrzkverzekeringstypes"
        managed = False

    def is_activity_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.ACTIVITY

    def is_temporary_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.TEMPORARY

    def is_travel_assistance_without_vehicle_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE

    def is_travel_assistance_with_vehicle_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE

    def is_temporary_vehicle_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.TEMPORARY_VEHICLE

    def is_equipment_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.EQUIPMENT

    def is_event_insurance(self) -> bool:
        return self.id == InsuranceTypeEnum.EVENT

    @staticmethod
    def get_non_member_types():
        return [
            InsuranceTypeEnum.EQUIPMENT,
            InsuranceTypeEnum.TEMPORARY,
            InsuranceTypeEnum.TEMPORARY_VEHICLE,
            InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE,
            InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE,
        ]
