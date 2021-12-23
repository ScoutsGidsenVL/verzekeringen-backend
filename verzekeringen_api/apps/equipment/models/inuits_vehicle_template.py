from django.db import models

from apps.equipment.managers import InuitsVehicleTemplateManager
from apps.equipment.models import InuitsVehicle

from scouts_insurances.insurances.models import TemporaryVehicleInsurance


class InuitsVehicleTemplate(models.Model):
    objects = InuitsVehicleTemplateManager()

    temporary_vehicle_insurance = models.OneToOneField(
        TemporaryVehicleInsurance, on_delete=models.CASCADE, primary_key=True, db_constraint=models.UniqueConstraint
    )
    inuits_vehicle = models.ForeignKey(InuitsVehicle, on_delete=models.CASCADE)
    editable = models.BooleanField(default=True)
