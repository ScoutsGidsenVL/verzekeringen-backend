import logging

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.people.services import InuitsNonMemberService

from apps.insurances.serializers import (
    InuitsTemporaryInsuranceSerializer,
    InuitsTravelAssistanceInsuranceSerializer,
    InuitsTemporaryVehicleInsuranceSerializer,
    InuitsEquipmentInsuranceSerializer, InuitsEventInsuranceSerializer, InuitsActivityInsuranceSerializer,
)

from scouts_insurances.insurances.models import BaseInsurance
from scouts_insurances.insurances.serializers import (
    BaseInsuranceSerializer,
    ActivityInsuranceSerializer,
    EventInsuranceSerializer, TemporaryInsuranceSerializer, EquipmentInsuranceSerializer,
)


logger = logging.getLogger(__name__)


class BaseInsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    inuits_non_member_service = InuitsNonMemberService()

    def get_queryset(self):
        return BaseInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceSerializer})
    def retrieve(self, request, pk=None):
        insurance: BaseInsurance = get_object_or_404(self.get_queryset(), pk=pk)

        if (
            insurance.type.is_temporary_insurance()
            or insurance.type.is_travel_assistance_without_vehicle_insurance()
            or insurance.type.is_travel_assistance_with_vehicle_insurance()
            or insurance.type.is_temporary_vehicle_insurance()
            or insurance.type.is_equipment_insurance()
        ):
            if insurance.type.is_temporary_insurance():
                serializer = TemporaryInsuranceSerializer(
                    insurance.temporary_child, context={"request": request}
                )
            elif (
                insurance.type.is_travel_assistance_without_vehicle_insurance()
                or insurance.type.is_travel_assistance_with_vehicle_insurance()
            ):
                serializer = InuitsTravelAssistanceInsuranceSerializer(
                    insurance.travel_assistance_child, context={"request": request}
                )
            elif insurance.type.is_temporary_vehicle_insurance():
                serializer = InuitsTemporaryVehicleInsuranceSerializer(
                    insurance.temporary_vehicle_child, context={"request": request}
                )
            elif insurance.type.is_equipment_insurance():
                serializer = EquipmentInsuranceSerializer(
                    insurance.equipment_child, context={"request": request}
                )
        elif insurance.type.is_activity_insurance():
            serializer = InuitsActivityInsuranceSerializer(insurance.activity_child, context={"request": request})
        elif insurance.type.is_event_insurance():
            serializer = InuitsEventInsuranceSerializer(insurance.event_child, context={"request": request})
        else:
            serializer = BaseInsuranceSerializer(insurance, many=True, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceSerializer})
    def list(self, request):
        # HACKETY HACK:
        # Since we don't approve or reject insurances, we can't catch when a NonMember
        # instance becomes non-editable. Check and fix it here when the list of
        # insurances is loaded
        self.inuits_non_member_service.check_editable_templates(user=request.user)

        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        # for insurance in insurances:
        #     logger.debug(insurance)

        if page is not None:
            serializer = BaseInsuranceSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BaseInsuranceSerializer(insurances, many=True)
            return Response(serializer.data)
