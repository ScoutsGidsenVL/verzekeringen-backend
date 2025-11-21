import logging

from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema

from apps.insurances.serializers import InuitsTravelAssistanceInsuranceSerializer
from apps.insurances.services import InuitsTravelAssistanceInsuranceService

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.models.enums import InsuranceStatus
from scouts_insurances.insurances.serializers import InsuranceCostSerializer


logger = logging.getLogger(__name__)


class InuitsTravelAssistanceInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    travel_assistance_insurance_service = InuitsTravelAssistanceInsuranceService()

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
        logger.debug("CREATE VALIDATED DATA FOR VEHICLE: %s", str(validated_data.get("vehicle")))

        created_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_create(
            **validated_data, created_by=request.user
        )
        output_serializer = InuitsTravelAssistanceInsuranceSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsTravelAssistanceInsuranceSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostSerializer},
    )
    @action(
        methods=["post"],
        detail=False,
        url_path="cost",
        permission_classes=[permissions.AllowAny]
    )
    def cost_calculation_travel_assistance(self, request):
        """
        Public API Endpoint to calculate cost of travel assistance insurance
        based on the amount of days, people and vehicles.
        """
        logger.debug("COST CALCULATION REQUEST DATA: %s", request.data)
        days_amount =  request.data.get("days_amount", 0)
        person_amount =  request.data.get("person_amount", 0)
        vehicle_amount = request.data.get("vehicle_amount", 0)

        cost = self.travel_assistance_insurance_service.calculate_total_cost(
            days_amount,
            person_amount,
            vehicle_amount,
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
        if existing_insurance._status != InsuranceStatus.BILLED:
            new_participants = list()
            for participant in request.data["participants"]:
                participant.pop("id", None)
                new_participants.append(participant)
            request.data["participants"] = new_participants
            input_serializer = InuitsTravelAssistanceInsuranceSerializer(
                data=request.data, context={"request": request}
            )
            input_serializer.is_valid(raise_exception=True)

            updated_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_update(
                insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
            )

            output_serializer = InuitsTravelAssistanceInsuranceSerializer(updated_insurance)

            return Response(output_serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise PermissionDenied({"message": f"Cannot edit insurance with status {str(InsuranceStatus.BILLED)}"})
