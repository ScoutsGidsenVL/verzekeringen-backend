import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.serializers import TravelAssistanceInsuranceSerializer, InsuranceCostSerializer
from scouts_insurances.insurances.services import TravelAssistanceInsuranceService


logger = logging.getLogger(__name__)


class TravelAssistanceInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    travel_assistance_insurance_service = TravelAssistanceInsuranceService()

    def get_queryset(self):
        return TravelAssistanceInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: TravelAssistanceInsuranceSerializer},
    )
    def create(self, request):
        input_serializer = TravelAssistanceInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TravelAssistanceInsuranceSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_travel_assistance(self, request):
        input_serializer = TravelAssistanceInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.travel_assistance_insurance_service.travel_assistance_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: TravelAssistanceInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TravelAssistanceInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = TravelAssistanceInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TravelAssistanceInsuranceSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
