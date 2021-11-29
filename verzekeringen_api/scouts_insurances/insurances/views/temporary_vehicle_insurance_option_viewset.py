from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models.enums import TemporaryVehicleInsuranceOptionApi

from scouts_auth.inuits.serializers import EnumSerializer


class TemporaryVehicleInsuranceOptionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        serializer = EnumSerializer(TemporaryVehicleInsuranceOptionApi.choices, many=True)
        return Response(serializer.data)
