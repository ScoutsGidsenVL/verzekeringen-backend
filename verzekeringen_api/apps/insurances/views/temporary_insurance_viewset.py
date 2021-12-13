import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models import TemporaryInsurance
from scouts_insurances.insurances.serializers import InsuranceCostSerializer, TemporaryInsuranceSerializer
from scouts_insurances.insurances.services import TemporaryInsuranceService


logger = logging.getLogger(__name__)


class TemporaryInsuranceViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    temporary_insurance_service = TemporaryInsuranceService()

    def get_queryset(self):
        return TemporaryInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceSerializer,
        responses={status.HTTP_201_CREATED: TemporaryInsuranceSerializer},
    )
    def create(self, request, *args, **kwargs):
        logger.debug("REQUEST DATA: %s", request.data)
        input_serializer = TemporaryInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("VALIDATED REQUEST DATA: %s", validated_data)

        created_insurance = self.temporary_insurance_service.temporary_insurance_create(
            **validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_temporary(self, request):
        input_serializer = TemporaryInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.temporary_insurance_service.temporary_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceSerializer,
        responses={status.HTTP_201_CREATED: TemporaryInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TemporaryInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = TemporaryInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.temporary_insurance_service.temporary_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
