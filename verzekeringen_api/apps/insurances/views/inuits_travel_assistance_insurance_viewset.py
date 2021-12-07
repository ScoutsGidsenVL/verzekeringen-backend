import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.serializers import InuitsTravelAssistanceInsuranceSerializer

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.serializers import InsuranceCostSerializer
from scouts_insurances.insurances.services import TravelAssistanceInsuranceService


logger = logging.getLogger(__name__)


class InuitsTravelAssistanceInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    travel_assistance_insurance_service = TravelAssistanceInsuranceService()

    def get_queryset(self):
        return TravelAssistanceInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=InuitsTravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InuitsTravelAssistanceInsuranceSerializer},
    )
    def create(self, request):
        logger.debug("CREATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsTravelAssistanceInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CREATE VALIDATED DATA: %s", validated_data)

        created_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_create(
            **validated_data, created_by=request.user
        )

        output_serializer = InuitsTravelAssistanceInsuranceSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsTravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_travel_assistance(self, request):
        logger.debug("COST CALCULATION REQUEST DATA: %s", request.data)
        input_serializer = InuitsTravelAssistanceInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("COST CALCULATION VALIDATED DATA: %s", validated_data)

        cost = self.travel_assistance_insurance_service.travel_assistance_insurance_cost_calculation(
            **validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsTravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InuitsTravelAssistanceInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TravelAssistanceInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = InuitsTravelAssistanceInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InuitsTravelAssistanceInsuranceSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
