from django.db import models

from scouts_insurances.equipment.models import Equipment

from apps.equipment.models import InuitsEquipment


class InuitsEquipmentTemplate(models.Model):
    equipment = models.OneToOneField(
        Equipment, on_delete=models.CASCADE, primary_key=True, db_constraint=models.UniqueConstraint
    )
    inuits_equipment = models.ForeignKey(InuitsEquipment, on_delete=models.CASCADE)
