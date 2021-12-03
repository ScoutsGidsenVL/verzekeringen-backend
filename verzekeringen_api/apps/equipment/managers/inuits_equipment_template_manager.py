from django.conf import settings
from django.db import models


class InuitsEquipmentTemplateQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(owner_group_group_admin_id__in=user_group_ids)


class InuitsEquipmentTemplateManager(models.Manager):
    def get_queryset(self):
        return InuitsEquipmentTemplateQuerySet(self.model, using=self._db)
