import logging
from django_filters import rest_framework as filters
from django.db.models import Q

from apps.insurances.models import InsuranceClaim

logger = logging.getLogger(__name__)


class InsuranceClaimFilter(filters.FilterSet):
    class Meta:
        model = InsuranceClaim
        fields = []

    @property
    def qs(self):
        parent = super().qs

        year_of_accident = self.request.query_params.get("year", None)
        # 83797
        # 79995 Section leader can see all claims for all authorized groups
        # @TODO also for group leader groups
        groups: list = [group.group_admin_id for group in self.request.user.get_section_leader_groups()]
        if year_of_accident and groups:
            logger.debug(
                "Filtering InsuranceClaim instance with year %s and groups [%s]", year_of_accident, ", ".join(groups)
            )
            return parent.filter(Q(date_of_accident__year=year_of_accident) | Q(group_group_admin_id__in=groups))

        if year_of_accident:
            logger.debug("Filtering InsuranceClaim instances with year %s", year_of_accident)
            return parent.filter(date_of_accident__year=year_of_accident)

        if groups:
            logger.debug("Filtering InsuranceClaim instances with groups [%s]", ", ".join(groups))
            return parent.filter(Q(group_group_admin_id__in=groups))

        return parent.all()
