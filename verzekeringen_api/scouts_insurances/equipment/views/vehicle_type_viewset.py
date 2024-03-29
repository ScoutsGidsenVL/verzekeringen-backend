from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from scouts_insurances.equipment.models import VehicleType

from scouts_auth.inuits.serializers import EnumSerializer


class VehicleTypeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        serializer = EnumSerializer(VehicleType.choices, many=True)
        return Response(serializer.data)
