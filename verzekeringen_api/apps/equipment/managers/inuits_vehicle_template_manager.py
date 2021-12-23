from django.conf import settings
from django.db import models
from django.db.models import Q


class InuitsVehicleTemplateQuerySet(models.QuerySet):
    def editable(self, inuits_vehicle=None):
        if not inuits_vehicle:
            return self.filter(editable=True)

        return self.filter(Q(editable=True) & Q(inuits_vehicle=inuits_vehicle))

    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(owner_group_group_admin_id__in=user_group_ids)


class InuitsVehicleTemplateManager(models.Manager):
    def get_queryset(self):
        return InuitsVehicleTemplateQuerySet(self.model, using=self._db)
