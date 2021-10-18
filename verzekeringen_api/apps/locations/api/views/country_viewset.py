from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.locations.models import Country
from apps.locations.api.filters import CountryFilter
from apps.locations.api.serializers import CountryOutputSerializer


class CountryViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = CountryFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return Country.objects.all()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CountryOutputSerializer},
    )
    @action(methods=["get"], detail=False, url_path="countries_by_type/(?P<type_id>\d+)")
    def get_by_type(self, request, type_id=None):
        countries = self.filter_queryset(self.get_queryset().by_type(type_id))
        page = self.paginate_queryset(countries)

        if page is not None:
            serializer = CountryOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CountryOutputSerializer(countries, many=True)
            return Response(serializer.data)
