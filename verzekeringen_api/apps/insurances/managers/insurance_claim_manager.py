import logging

from django.conf import settings
from django.db import models


logger = logging.getLogger(__name__)


class InsuranceClaimQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        logger.debug("RETURNING INSURANCE CLAIM QUERYSET allowed")
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=user_group_ids)


class InsuranceClaimManager(models.Manager):
    def get_queryset(self):
        logger.debug("Returning INSURANCE CLAIM QUERYSET")
        return InsuranceClaimQuerySet(self.model, using=self._db).order_by("date_of_accident")
