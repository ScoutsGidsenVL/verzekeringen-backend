import django_filters
from django.db.models.functions import Concat
from django.db.models import CharField, Value, Q

from apps.equipment.models import InuitsVehicle, InuitsEquipment


class InuitsVehicleFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(method="search_term_filter")

    class Meta:
        model = InuitsVehicle
        fields = []

    def search_term_filter(self, queryset, name, value):
        # Annotate brand and license_plate so we can do an icontains on entire string
        return (
            queryset.annotate(brand_license_plate=Concat("brand", Value(" "), "license_plate"))
            .annotate(license_plate_brand=Concat("license_plate", Value(" "), "brand"))
            .filter(
                Q(brand_license_plate__icontains=value)
                | Q(license_plate_brand__icontains=value)
                | Q(chassis_number__icontains=value),
                output_field=CharField(),
            )
        )


class InuitsEquipmentFilter(django_filters.FilterSet):
    term = django_filters.CharFilter(method="search_term_filter")

    class Meta:
        model = InuitsEquipment
        fields = []

    def search_term_filter(self, queryset, name, value):
        return queryset.filter(Q(nature__icontains=value) | Q(description__icontains=value))
