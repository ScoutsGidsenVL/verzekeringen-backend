from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOptionApi


class TemporaryVehicleInsuranceOptionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        serializer = EnumSerializer(TemporaryVehicleInsuranceOptionApi.choices, many=True)
        return Response(serializer.data)
