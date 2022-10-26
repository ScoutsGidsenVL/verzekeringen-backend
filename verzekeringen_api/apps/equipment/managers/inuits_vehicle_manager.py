from django.conf import settings
from django.db import models

from scouts_insurances.insurances.models import TemporaryVehicleInsurance


class InuitsVehicleQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        insurances = TemporaryVehicleInsurance.objects.filter(_group_group_admin_id__in=user_group_ids)
        allowed_vehicle_ids = list()
        for insurance in insurances:
            allowed_vehicle_ids.append(insurance._vehicle_id)
        return self.filter(id__in=allowed_vehicle_ids)


class InuitsVehicleManager(models.Manager):
    def get_queryset(self):
        return InuitsVehicleQuerySet(self.model, using=self._db)
