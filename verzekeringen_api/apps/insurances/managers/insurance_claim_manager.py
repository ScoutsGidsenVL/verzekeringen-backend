from django.conf import settings
from django.db import models


class InsuranceClaimQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_number__in=user_group_ids)


class InsuranceClaimManager(models.Manager):
    def get_queryset(self):
        return InsuranceClaimQuerySet(self.model, using=self._db)
