from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicleTrailerOption

from scouts_auth.inuits.serializers import EnumSerializer


class VehicleTrailerOptionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        # We filter out one because it should not be used anymore
        serializer = EnumSerializer(
            [choice for choice in TemporaryVehicleInsuranceVehicleTrailerOption.choices if choice != "1"], many=True
        )
        return Response(serializer.data)
