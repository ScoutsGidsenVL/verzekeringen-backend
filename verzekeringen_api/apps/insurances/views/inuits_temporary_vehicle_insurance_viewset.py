import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from apps.insurances.serializers import InuitsTemporaryVehicleInsuranceSerializer
from apps.insurances.services import InuitsTemporaryVehicleInsuranceService

from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.models.enums import InsuranceStatus
from scouts_insurances.insurances.serializers import InsuranceCostSerializer


logger = logging.getLogger(__name__)


class InuitsTemporaryVehicleInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    temporary_vehicle_insurance_service = InuitsTemporaryVehicleInsuranceService()

    def get_queryset(self):
        return TemporaryVehicleInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=InuitsTemporaryVehicleInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InuitsTemporaryVehicleInsuranceSerializer},
    )
    def create(self, request):
        logger.debug("REQUEST DATA: %s", request.data)
        input_serializer = InuitsTemporaryVehicleInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("VALIDATED REQUEST DATA: %s", validated_data)

        created_insurance = self.temporary_vehicle_insurance_service.temporary_vehicle_insurance_create(
            **validated_data, created_by=request.user
        )

        output_serializer = InuitsTemporaryVehicleInsuranceSerializer(created_insurance, context=created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsTemporaryVehicleInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_temporary_vehicle(self, request):
        logger.debug("COST CALCULATION REQUEST DATA: %s", request.data)
        input_serializer = InuitsTemporaryVehicleInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("COST CALCULATION VALIDATED REQUEST DATA: %s", validated_data)

        cost = self.temporary_vehicle_insurance_service.temporary_vehicle_insurance_cost_calculation(
            **validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsTemporaryVehicleInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InuitsTemporaryVehicleInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TemporaryVehicleInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        if existing_insurance._status != InsuranceStatus.BILLED:

            input_serializer = InuitsTemporaryVehicleInsuranceSerializer(data=request.data, context={"request": request})
            input_serializer.is_valid(raise_exception=True)

            updated_insurance = self.temporary_vehicle_insurance_service.temporary_vehicle_insurance_update(
                insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
            )

            output_serializer = InuitsTemporaryVehicleInsuranceSerializer(updated_insurance)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied(
                {
                    "message": f"Cannot edit insurance with status {str(InsuranceStatus.BILLED)}"
                }
            )