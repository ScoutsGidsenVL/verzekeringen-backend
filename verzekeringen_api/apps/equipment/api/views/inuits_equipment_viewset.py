from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import (
    InuitsEquipmentDetailOutputSerializer,
    InuitsEquipmentListOutputSerializer,
    InuitsEquipmentCreateInputSerializer,
)
from ..filters import InuitsEquipmentFilter
from ...services import EquipmentService
from ...models import InuitsEquipment


class InuitsEquipmentViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsEquipmentFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return InuitsEquipment.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsEquipmentDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        equipment = self.get_object()
        serializer = InuitsEquipmentDetailOutputSerializer(equipment, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsEquipmentListOutputSerializer})
    def list(self, request):
        equipment = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(equipment)

        if page is not None:
            serializer = InuitsEquipmentListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsEquipmentListOutputSerializer(equipment, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsEquipmentCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InuitsEquipmentDetailOutputSerializer},
    )
    def create(self, request):
        input_serializer = InuitsEquipmentCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_equipment = EquipmentService.inuits_equipment_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InuitsEquipmentDetailOutputSerializer(created_equipment, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)