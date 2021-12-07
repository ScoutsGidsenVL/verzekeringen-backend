from django.db import models

from scouts_insurances.insurances.models.enums import InsuranceTypeEnum


class InsuranceTypeManager(models.Manager):
    def get_queryset(self):
        # Exclude some types from list that may still be in database
        return super().get_queryset().exclude(id__in=[11, 12])

    def activity(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.ACTIVITY)

    def temporary(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.TEMPORARY)

    def travel_assistance_without_vehicle(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE)

    def travel_assistance_with_vehicle(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE)

    def temporary_vehicle(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.TEMPORARY_VEHICLE)

    def equipment(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.EQUIPMENT)

    def event(self):
        return self.get_queryset().get(id=InsuranceTypeEnum.EVENT)
