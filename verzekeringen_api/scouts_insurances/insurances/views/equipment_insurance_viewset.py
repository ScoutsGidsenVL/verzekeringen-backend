import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models import BaseInsurance, EquipmentInsurance
from scouts_insurances.insurances.serializers import InsuranceCostSerializer, EquipmentInsuranceSerializer
from scouts_insurances.insurances.services import EquipmentInsuranceService


logger = logging.getLogger(__name__)


class EquipmentInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    equipment_insurance_service = EquipmentInsuranceService()

    def get_queryset(self):
        return EquipmentInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=EquipmentInsuranceSerializer,
        responses={status.HTTP_201_CREATED: EquipmentInsuranceSerializer},
    )
    def create(self, request):
        input_serializer = EquipmentInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = self.equipment_insurance_service.equipment_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EquipmentInsuranceSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EquipmentInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_equipment(self, request):
        input_serializer = EquipmentInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.equipment_insurance_service.equipment_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EquipmentInsuranceSerializer,
        responses={status.HTTP_201_CREATED: EquipmentInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            EquipmentInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = EquipmentInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.equipment_insurance_service.equipment_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EquipmentInsuranceSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
