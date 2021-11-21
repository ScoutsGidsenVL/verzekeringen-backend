import logging

from django.db.models.functions import Concat
from django.db.models import Value, Q
from django_filters import FilterSet, CharFilter, DateTimeFilter

from apps.members.models import InuitsNonMember


logger = logging.getLogger(__name__)


class InuitsNonMemberFilter(FilterSet):
    term = CharFilter(method="search_term_filter")
    start = DateTimeFilter(method="search_insurance_start_filter")
    end = DateTimeFilter(method="search_insurance_end_filter")

    class Meta:
        model = InuitsNonMember
        fields = []

    def search_term_filter(self, queryset, name, value):
        # Annotate full name so we can do an icontains on the entire name
        return (
            queryset.annotate(full_name_1=Concat("first_name", Value(" "), "last_name"))
            .annotate(full_name_2=Concat("last_name", Value(" "), "first_name"))
            .filter(Q(full_name_1__icontains=value) | Q(full_name_2__icontains=value))
        )

    def search_insurance_start_filter(self, queryset, name, value):
        logger.debug("Filtering non_members with an insurance that started on %s", value)

    def search_insurance_end_filter(self, queryset, name, value):
        logger.debug("Filtering non_members with an insurance that ended on %s", value)
