import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.equipment.serializers import InuitsVehicleSerializer
from apps.equipment.filters import InuitsVehicleFilter
from apps.equipment.services import InuitsVehicleService
from apps.equipment.models import InuitsVehicle


logger = logging.getLogger(__name__)


class InuitsVehicleViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsVehicleFilter
    ordering_fields = ["brand", "license_plate", "chassis_number"]
    ordering = ["brand", "license_plate", "chassis_number"]

    service = InuitsVehicleService()

    def get_queryset(self):
        return InuitsVehicle.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsVehicleSerializer})
    def retrieve(self, request, pk=None):
        vehicle = self.get_object()
        serializer = InuitsVehicleSerializer(vehicle)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsVehicleSerializer})
    def list(self, request):
        vehicles = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(vehicles)

        if page is not None:
            serializer = InuitsVehicleSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsVehicleSerializer(vehicles, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsVehicleSerializer,
        responses={status.HTTP_201_CREATED: InuitsVehicleSerializer},
    )
    def create(self, request):
        logger.debug("CREATE REQUEST DATA: %s", request.data)
        input_serializer = InuitsVehicleSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CREATE VALIDATED DATA: %s", validated_data)

        created_vehicle = self.service.inuits_vehicle_create(**validated_data, created_by=request.user)

        output_serializer = InuitsVehicleSerializer(created_vehicle, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsVehicleSerializer,
        responses={status.HTTP_200_OK: InuitsVehicleSerializer},
    )
    def partial_update(self, request, pk=None):
        vehicle = self.get_object()

        serializer = InuitsVehicleSerializer(
            data=request.data, instance=vehicle, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_vehicle = self.service.inuits_vehicle_update(vehicle=vehicle, **serializer.validated_data)

        output_serializer = InuitsVehicleSerializer(updated_vehicle)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
