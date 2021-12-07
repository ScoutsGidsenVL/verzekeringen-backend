from datetime import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings


class InuitsNonMemberQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        groups = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(
            # Equipment (vrzkmateriaal)
            Q(template__non_member__equipment__insurance__insurance_parent___group_group_admin_id__in=groups)
            # NonMemberTemporaryInsurance (vrzknietledentijd)
            | Q(
                template__non_member__temporary__temporary_insurance__insurance_parent___group_group_admin_id__in=groups
            )
            # ParticipantTemporaryVehicleInsurance (vrzktijdautonietleden)
            | Q(template__non_member__temporary_vehicle__insurance__insurance_parent___group_group_admin_id__in=groups)
            # ParticipantTravelAssistanceInsurance (vrzkassistpassagier)
            | Q(template__non_member__travel__temporary_insurance__insurance_parent___group_group_admin_id__in=groups)
        )

    def currently_insured(self, start: datetime, end: datetime):
        return self.filter(
            # Equipment (vrzkmateriaal)
            (
                Q(template__non_member__equipment__insurance__insurance_parent__start_date__gte=start)
                and Q(template__non_member__equipment__insurance__insurance_parent__end_date__lte=end)
            )
            # NonMemberTemporaryInsurance (vrzknietledentijd)
            | (
                Q(template__non_member__temporary__temporary_insurance__insurance_parent__start_date__gte=start)
                and Q(template__non_member__temporary__temporary_insurance__insurance_parent__end_date__lte=end)
            )
            # ParticipantTemporaryVehicleInsurance (vrzktijdautonietleden)
            | (
                Q(template__non_member__temporary_vehicle__insurance__insurance_parent__start_date__gte=start)
                and Q(template__non_member__temporary_vehicle__insurance__insurance_parent__end_date__lte=end)
            )
            # ParticipantTravelAssistanceInsurance (vrzkassistpassagier)
            | (
                Q(template__non_member__travel__temporary_insurance__insurance_parent__start_date__gte=start)
                and Q(template__non_member__travel__temporary_insurance__insurance_parent__end_date__lte=end)
            )
        )


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        return InuitsNonMemberQuerySet(self.model, using=self._db)
