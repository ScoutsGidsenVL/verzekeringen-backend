import django_filters
from django.db.models.functions import Concat
from django.db.models import Value, Q
from ..models import Country


class CountryFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Country
        fields = []
