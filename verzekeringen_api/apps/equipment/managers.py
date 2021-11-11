from django.db import models


class InuitsVehicleQuerySet(models.QuerySet):
    def allowed(self, user):
        user_group_ids = [group.id for group in user.partial_scouts_groups]
        return self.filter(group_number__in=user_group_ids)


class InuitsVehicleManager(models.Manager):
    def get_queryset(self):
        return InuitsVehicleQuerySet(self.model, using=self._db)


class InuitsEquipmentQuerySet(models.QuerySet):
    def allowed(self, user):
        user_group_ids = [group.id for group in user.partial_scouts_groups]
        return self.filter(group_number__in=user_group_ids)


class InuitsEquipmentManager(models.Manager):
    def get_queryset(self):
        return InuitsEquipmentQuerySet(self.model, using=self._db)
