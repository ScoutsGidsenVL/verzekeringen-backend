import logging
from django_filters import rest_framework as filters
from django.db.models import Q

from ..models.insurance_claim import InsuranceClaim

logger = logging.getLogger(__name__)


class InsuranceClaimFilter(filters.FilterSet):
    class Meta:
        model = InsuranceClaim
        fields = []

    @property
    def qs(self):
        parent = super().qs

        year_of_accident = self.request.query_params.get("year", None)

        if year_of_accident:
            logger.debug("Filtering InsuranceClaim instances with year %s", year_of_accident)
            return parent.filter(date_of_accident__year=year_of_accident)

        return parent.all()
