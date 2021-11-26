from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator

from scouts_insurances.insurances.models import InsuranceType


class CostVariableQuerySet(models.QuerySet):
    def get_variable(self, insurance_type, key):
        return self.get(insurance_type=insurance_type, key=key)


class CostVariableManager(models.Manager):
    def get_queryset(self):
        return CostVariableQuerySet(self.model, using=self._db)

    def get_variable(self, insurance_type, key):
        return self.get_queryset().get_variable(insurance_type, key)


class CostVariable(models.Model):
    objects = CostVariableManager()

    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=30)
    value = models.DecimalField(
        max_digits=8,
        decimal_places=5,
        validators=[MinValueValidator(Decimal("0"))],
    )
    insurance_type = models.ForeignKey(InsuranceType, on_delete=models.RESTRICT, related_name="cost_variables")

    class Meta:
        unique_together = ("key", "insurance_type")
