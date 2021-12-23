from django.db import models

from apps.equipment.managers import InuitsEquipmentTemplateManager
from apps.equipment.models import InuitsEquipment

from scouts_insurances.equipment.models import Equipment


class InuitsEquipmentTemplate(models.Model):
    objects = InuitsEquipmentTemplateManager()

    equipment = models.OneToOneField(
        Equipment,
        on_delete=models.CASCADE,
        primary_key=True,
        db_constraint=models.UniqueConstraint,
        related_name="template",
    )
    inuits_equipment = models.ForeignKey(InuitsEquipment, on_delete=models.CASCADE, related_name="template")
    editable = models.BooleanField(default=True)
