from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import InuitsVehicleOutputSerializer, InuitsVehicleCreateInputSerializer
from ..filters import InuitsVehicleFilter
from ...services import VehicleService
from ...models import InuitsVehicle


class VehicleViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsVehicleFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return InuitsVehicle.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsVehicleOutputSerializer})
    def retrieve(self, request, pk=None):
        vehicle = self.get_object()
        serializer = InuitsVehicleOutputSerializer(vehicle)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsVehicleOutputSerializer})
    def list(self, request):
        vehicles = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(vehicles)

        if page is not None:
            serializer = InuitsVehicleOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsVehicleOutputSerializer(vehicles, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsVehicleCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InuitsVehicleOutputSerializer},
    )
    def create(self, request):
        input_serializer = InuitsVehicleCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_vehicle = VehicleService.inuits_vehicle_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InuitsVehicleOutputSerializer(created_vehicle, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
