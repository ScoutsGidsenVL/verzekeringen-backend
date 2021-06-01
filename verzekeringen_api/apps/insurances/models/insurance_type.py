from django.db import models


class InsuranceTypeManager(models.Manager):
    def get_queryset(self):
        # Exclude some types from list that may still be in database
        return super().get_queryset().exclude(id__in=[11, 12])

    def activity(self):
        return self.get_queryset().get(id=1)

    def temporary(self):
        return self.get_queryset().get(id=2)


class InsuranceType(models.Model):
    objects = InsuranceTypeManager()

    id = models.IntegerField(db_column="verzekeringstypeid", primary_key=True)
    name = models.CharField(db_column="verzekeringstype", max_length=30)
    description = models.CharField(db_column="verzekeringstypeomschr", max_length=50)
    max_term = models.CharField(db_column="maxtermijn", max_length=10)

    class Meta:
        db_table = "vrzkverzekeringstypes"
        managed = False
