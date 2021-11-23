import logging

from django.conf import settings
from django.db import models


logger = logging.getLogger(__name__)


class InsuranceClaimQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        # Administrators can see all claims
        if user.has_role_administrator():
            return self.qs

        # Section and group leaders can see all claims, but only for authorized groups
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=user_group_ids)


class InsuranceClaimManager(models.Manager):
    def get_queryset(self):
        return InsuranceClaimQuerySet(self.model, using=self._db).order_by("date_of_accident")
