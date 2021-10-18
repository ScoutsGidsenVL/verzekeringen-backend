import django_filters

from apps.locations.models import Country


class CountryFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Country
        fields = []
