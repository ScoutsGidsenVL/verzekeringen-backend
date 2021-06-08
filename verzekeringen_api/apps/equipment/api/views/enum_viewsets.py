from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from apps.base.serializers import EnumOutputSerializer
from ...enums import VehicleType, VehicleTrailerOption


class VehicleTypeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(VehicleType.choices, many=True)
        return Response(serializer.data)


class VehicleTrailerOptionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        # We filter out one because it should not be used anymore
        serializer = EnumOutputSerializer(
            [choice for choice in VehicleTrailerOption.choices if choice != "1"], many=True
        )
        return Response(serializer.data)
