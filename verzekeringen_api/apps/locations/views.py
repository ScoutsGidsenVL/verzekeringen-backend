from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.locations.models import Country
from apps.locations.filters import CountryFilter
from apps.locations.serializers import CountrySerializer, BelgianPostalCodeCitySerializer
from apps.locations.services import BelgianPostalCodeCityService


class CountryViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = CountryFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return Country.objects.all()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: CountrySerializer},
    )
    @action(methods=["get"], detail=False, url_path="countries_by_type/(?P<type_id>\d+)")
    def get_by_type(self, request, type_id=None):
        countries = self.filter_queryset(self.get_queryset().by_type(type_id))
        page = self.paginate_queryset(countries)

        if page is not None:
            serializer = CountrySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = CountrySerializer(countries, many=True)
            return Response(serializer.data)


class BelgianPostalCodeCitySearch(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: BelgianPostalCodeCitySerializer})
    def get(self, request):
        search_term = self.request.GET.get("term", None)
        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")
        results = BelgianPostalCodeCityService().search(term=search_term)
        output_serializer = BelgianPostalCodeCitySerializer(results, many=True)

        return Response(output_serializer.data)
