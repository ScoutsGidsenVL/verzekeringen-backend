from django.db import models


class InsuranceTypeManager(models.Manager):
    def get_queryset(self):
        # Exclude some types from list that may still be in database
        return super().get_queryset().exclude(id__in=[11, 12])

    def activity(self):
        return self.get_queryset().get(id=1)

    def temporary(self):
        return self.get_queryset().get(id=2)

    def travel_assistance_without_vehicle(self):
        return self.get_queryset().get(id=3)

    def travel_assistance_with_vehicle(self):
        return self.get_queryset().get(id=4)

    def temporary_vehicle(self):
        return self.get_queryset().get(id=5)

    def equipment(self):
        return self.get_queryset().get(id=6)

    def event(self):
        return self.get_queryset().get(id=10)


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
        return self.id == 1

    def is_temporary_insurance(self) -> bool:
        return self.id == 2

    def is_travel_assistance_without_vehicle_insurance(self) -> bool:
        return self.id == 3

    def is_travel_assistance_with_vehicle_insurance(self) -> bool:
        return self.id == 4

    def is_temporary_vehicle_insurance(self) -> bool:
        return self.id == 5

    def is_equipment_insurance(self) -> bool:
        return self.id == 6

    def is_event_insurance(self) -> bool:
        return self.id == 10
