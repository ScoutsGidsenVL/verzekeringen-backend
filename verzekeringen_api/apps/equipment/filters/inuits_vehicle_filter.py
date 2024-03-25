import django_filters
from django.db.models import Q
from django.db.models.functions import Concat

from apps.equipment.models import InuitsVehicle


class InuitsVehicleFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(method="search_term_filter")

    class Meta:
        model = InuitsVehicle
        fields = []

    def search_term_filter(self, queryset, name, value):
        # Annotate brand and license_plate so we can do an icontains on entire string
        return (
            queryset.annotate(brand_license_plate=Concat("brand", "license_plate"))
            .annotate(license_plate_brand=Concat("license_plate", "brand"))
            .filter(
                Q(brand_license_plate__icontains=value)
                | Q(license_plate_brand__icontains=value)
                | Q(chassis_number__icontains=value)
            )
        )
