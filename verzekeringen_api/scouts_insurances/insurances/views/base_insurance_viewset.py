import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models import BaseInsurance
from scouts_insurances.insurances.serializers import (
    BaseInsuranceSerializer,
    ActivityInsuranceSerializer,
    TemporaryInsuranceSerializer,
    TravelAssistanceInsuranceSerializer,
    TemporaryVehicleInsuranceSerializer,
    EventInsuranceSerializer,
    EquipmentInsuranceSerializer,
)


logger = logging.getLogger(__name__)


class BaseInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    def get_queryset(self):
        return BaseInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceSerializer})
    def retrieve(self, request, pk=None):
        insurance: BaseInsurance = get_object_or_404(self.get_queryset(), pk=pk)

        if insurance.type.id == 1:
            serializer = ActivityInsuranceSerializer(insurance.activity_child, context={"request": request})
        elif insurance.type.id == 2:
            serializer = TemporaryInsuranceSerializer(insurance.temporary_child, context={"request": request})
        elif insurance.type.id in (3, 4):
            serializer = TravelAssistanceInsuranceSerializer(
                insurance.travel_assistance_child, context={"request": request}
            )
        elif insurance.type.id == 5:
            serializer = TemporaryVehicleInsuranceSerializer(
                insurance.temporary_vehicle_child, context={"request": request}
            )
        elif insurance.type.id == 6:
            serializer = EquipmentInsuranceSerializer(insurance.equipment_child, context={"request": request})
        elif insurance.type.id == 10:
            serializer = EventInsuranceSerializer(insurance.event_child, context={"request": request})
        else:
            serializer = BaseInsuranceSerializer(insurance, many=True, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        for insurance in insurances:
            logger.debug(insurance)

        if page is not None:
            serializer = BaseInsuranceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BaseInsuranceSerializer(insurances, many=True)
            return Response(serializer.data)
