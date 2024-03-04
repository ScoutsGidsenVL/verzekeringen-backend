from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from scouts_insurances.insurances.models import InsuranceType
from scouts_insurances.insurances.serializers import InsuranceTypeSerializer


class InsuranceTypeViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return InsuranceType.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceTypeSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InsuranceTypeSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceTypeSerializer})
    def list(self, request):
        types = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(types)

        if page is not None:
            serializer = InsuranceTypeSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InsuranceTypeSerializer(types, many=True)
            return Response(serializer.data)
