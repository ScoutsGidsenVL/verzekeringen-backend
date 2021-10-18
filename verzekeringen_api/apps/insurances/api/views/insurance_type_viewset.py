from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.api.serializers import InsuranceTypeOutputSerializer
from apps.insurances.models import InsuranceType


class InsuranceTypeViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return InsuranceType.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceTypeOutputSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InsuranceTypeOutputSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceTypeOutputSerializer})
    def list(self, request):
        types = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(types)

        if page is not None:
            serializer = InsuranceTypeOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InsuranceTypeOutputSerializer(types, many=True)
            return Response(serializer.data)
