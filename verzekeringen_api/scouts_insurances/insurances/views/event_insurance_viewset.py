import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models import BaseInsurance, EventInsurance
from scouts_insurances.insurances.serializers import InsuranceCostSerializer, EventInsuranceSerializer
from scouts_insurances.insurances.services import EventInsuranceService


logger = logging.getLogger(__name__)


class EventInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    event_insurance_service = EventInsuranceService()

    def get_queryset(self):
        return EventInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=EventInsuranceSerializer,
        responses={status.HTTP_201_CREATED: EventInsuranceSerializer},
    )
    def create(self, request):
        logger.debug("CREATE DATA: %s", request.data)
        input_serializer = EventInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("VALIDATED DATA: %s", validated_data)

        created_insurance = self.event_insurance_service.event_insurance_create(
            **validated_data, created_by=request.user
        )

        output_serializer = EventInsuranceSerializer(created_insurance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(methods=["post"], detail=False, url_path="cost")
    def cost_calculation_event(self, request):
        logger.debug("COST CALCULATION DATA: %s", request.data)
        input_serializer = EventInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("COST CALCULATION VALIDATED DATA: %s", validated_data)

        cost = self.event_insurance_service.event_insurance_cost_calculation(**validated_data, created_by=request.user)

        output_serializer = InsuranceCostSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventInsuranceSerializer,
        responses={status.HTTP_201_CREATED: EventInsuranceSerializer},
    )
    def partial_update(self, request, pk=None):
        existing_insurance = get_object_or_404(
            EventInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = EventInsuranceSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.event_insurance_service.event_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EventInsuranceSerializer(updated_insurance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
