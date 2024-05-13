import django_filters
from apps.equipment.models import InuitsEquipment
from django.db.models import Q


class InuitsEquipmentFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(method="search_term_filter")

    class Meta:
        model = InuitsEquipment
        fields = []

    def search_term_filter(self, queryset, name, value):
        return queryset.filter(Q(nature__icontains=value) | Q(description__icontains=value))
