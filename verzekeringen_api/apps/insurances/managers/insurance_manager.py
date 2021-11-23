import logging
from datetime import datetime, timedelta

from django.conf import settings
from django.db import models

from apps.insurances.models.enums import InsuranceStatus


logger = logging.getLogger(__name__)


class BaseInsuranceQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        # Administrators can see all claims
        if user.has_role_administrator():
            return self.qs

        # Section and group leaders can view and change requests they made themselves
        section_leader_groups = [group.group_admin_id for group in user.get_section_leader_groups()]
        group_leader_groups = [group.group_admin_id for group in user.get_group_leader_groups()]
        groups = section_leader_groups + list(set(group_leader_groups) - set(section_leader_groups))
        return self.filter(_group_group_admin_id__in=groups)

    def editable(self, user: settings.AUTH_USER_MODEL):
        # Only section leaders can edit and only their own requests
        # Insurance requests can't be edited after they've been approved or invoiced
        return self.filter(
            _status__in=[InsuranceStatus.NEW, InsuranceStatus.WAITING], responsible_member__ga_id=user.id
        )


class BaseInsuranceManager(models.Manager):
    def get_queryset(self):
        return (
            BaseInsuranceQuerySet(self.model, using=self._db)
            .filter(created_on__gte=datetime.now() - timedelta(days=3 * 365))
            .order_by("created_on")
        )
