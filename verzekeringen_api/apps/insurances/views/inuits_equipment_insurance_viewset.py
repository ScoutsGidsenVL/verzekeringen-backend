import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.serializers import InuitsEquipmentInsuranceSerializer
from apps.insurances.services import InuitsEquipmentInsuranceService

from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.serializers import InsuranceCostSerializer


logger = logging.getLogger(__name__)


class InuitsEquipmentInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    equipment_insurance_service = InuitsEquipmentInsuranceService()

    def get_queryset(self):
        return EquipmentInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=InuitsEquipmentInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InuitsEquipmentInsuranceSerializer},
    )
    def create(self, request):
        logger.debug("CREATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsEquipmentInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CREATE VALIDATED DATA: %s", validated_data)

        created_insurance = self.equipment_insurance_service.inuits_equipment_insurance_create(
            **validated_data, created_by=request.user
        )

        output_serializer = InuitsEquipmentInsuranceSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsEquipmentInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_equipment(self, request):
        logger.debug("COST CALCULATION REQUEST DATA: %s", request.data)
        input_serializer = InuitsEquipmentInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("COST CALCULATION VALIDATED DATA: %s", validated_data)

        cost = self.equipment_insurance_service.equipment_insurance_cost_calculation(
            **validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsEquipmentInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InuitsEquipmentInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            EquipmentInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )

        logger.debug("UPDATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsEquipmentInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("UPDATE VALIDATED DATA: %s", validated_data)

        updated_insurance = self.equipment_insurance_service.inuits_equipment_insurance_update(
            insurance=existing_insurance, **validated_data, created_by=request.user
        )

        output_serializer = InuitsEquipmentInsuranceSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
