from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.base.serializers import EnumOutputSerializer
from apps.equipment.enums import VehicleType, VehicleTrailerOption


class VehicleTypeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(VehicleType.choices, many=True)
        return Response(serializer.data)


class VehicleTrailerOptionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        # We filter out one because it should not be used anymore
        serializer = EnumOutputSerializer(
            [choice for choice in VehicleTrailerOption.choices if choice != "1"], many=True
        )
        return Response(serializer.data)
