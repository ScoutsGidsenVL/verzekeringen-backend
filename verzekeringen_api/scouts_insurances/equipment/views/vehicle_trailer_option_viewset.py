from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_insurances.equipment.models import TemporaryVehicleInsuranceVehicleTrailerOption


class VehicleTrailerOptionViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        # We filter out one because it should not be used anymore
        serializer = EnumSerializer(
            [choice for choice in TemporaryVehicleInsuranceVehicleTrailerOption.choices if choice != "1"], many=True
        )
        return Response(serializer.data)
