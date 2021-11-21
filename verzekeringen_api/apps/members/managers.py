from datetime import date

from django.db import models
from django.conf import settings


class InuitsNonMemberQuerySet(models.QuerySet):
    # @TODO: is this necessary ?
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_number__in=user_group_ids)


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        return InuitsNonMemberQuerySet(self.model, using=self._db)

    def currently_insured(self, start: date, end: date):
        return self.get_queryset().filter()
