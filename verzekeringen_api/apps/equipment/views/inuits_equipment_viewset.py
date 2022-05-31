import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.equipment.filters import InuitsEquipmentFilter
from apps.equipment.serializers import InuitsEquipmentSerializer
from apps.equipment.services import InuitsEquipmentService
from apps.equipment.models import InuitsEquipment


logger = logging.getLogger(__name__)


class InuitsEquipmentViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsEquipmentFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = InuitsEquipmentService()

    def get_queryset(self):
        return InuitsEquipment.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsEquipmentSerializer})
    def retrieve(self, request, pk=None):
        equipment = self.get_object()
        serializer = InuitsEquipmentSerializer(equipment, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsEquipmentSerializer})
    def list(self, request):
        equipment = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(equipment)

        if page is not None:
            serializer = InuitsEquipmentSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsEquipmentSerializer(equipment, many=True, context={"request": request})
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsEquipmentSerializer,
        responses={status.HTTP_201_CREATED: InuitsEquipmentSerializer},
    )
    def create(self, request):
        logger.debug("CREATE DATA: %s", request.data)

        input_serializer = InuitsEquipmentSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("CREATE VALIDATED DATA: %s", validated_data)

        created_equipment = self.service.inuits_equipment_create(
            inuits_equipment=validated_data, created_by=request.user
        )

        output_serializer = InuitsEquipmentSerializer(created_equipment, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsEquipmentSerializer,
        responses={status.HTTP_200_OK: InuitsEquipmentSerializer},
    )
    def partial_update(self, request, pk=None):
        logger.debug("UPDATE REQUEST DATA: %s", request.data)
        equipment = self.get_object()

        serializer = InuitsEquipmentSerializer(
            data=request.data, instance=equipment, partial=True, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("UPDATE VALIDATED DATA: %s", validated_data)

        updated_equipment = self.service.inuits_equipment_update(
            inuits_equipment=equipment, updated_inuits_equipment=validated_data, updated_by=request.user
        )

        output_serializer = InuitsEquipmentSerializer(updated_equipment, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)
