from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from apps.base.serializers import EnumOutputSerializer
from ...enums import VehicleType


class VehicleTypeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(VehicleType.choices, many=True)
        return Response(serializer.data)
