from datetime import date, datetime

from django.db import models
from django.db.models import Q
from django.conf import settings


class InuitsNonMemberQuerySet(models.QuerySet):
    # @TODO: is this necessary ?
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_group_admin_id__in=user_group_ids)

    def with_group(self, group: str):
        return self.filter(group_group_admin_id=group)

    def currently_insured(self, start: datetime, end: datetime):
        return self.filter(
            (
                Q(template__non_member__equipment__equipment_child___start_date__gte=start)
                and Q(template__non_member__equipment__insurance_parent___end_date__lte=end)
            )
            | (
                Q(template__non_member__temporary__temporary_insurance__temporary_child___start_date__gte=start)
                and Q(template__non_member__temporary__temporary_insurance__temporary_child___end_date__lte=end)
            )
            | (
                Q(template__non_member__temporary_vehicle__insurance__insurance_parent___start_date__gte=start)
                and Q(template__non_member__temporary_vehicle__insurance__insurance_parent___end_date__lte=end)
            )
            | (
                Q(template__non_member__travel__temporary_insurance__insurance_parent___start_date__gte=start)
                and Q(template__non_member__travel__temporary_insurance__insurance_parent___end_date__lte=end)
            )
        )


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        return InuitsNonMemberQuerySet(self.model, using=self._db)
