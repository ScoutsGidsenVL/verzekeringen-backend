from datetime import date

from django.db import models
from django.conf import settings


class InuitsNonMemberQuerySet(models.QuerySet):
    # @TODO: is this necessary ?
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=user_group_ids)

    def with_group(self, group: str):
        return self.filter(group_group_admin_id=group)


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        return InuitsNonMemberQuerySet(self.model, using=self._db)

    def currently_insured(self, start: date, end: date):
        return self.get_queryset().filter()
