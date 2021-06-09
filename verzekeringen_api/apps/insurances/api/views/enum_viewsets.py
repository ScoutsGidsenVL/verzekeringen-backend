from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from apps.base.serializers import EnumOutputSerializer
from ...models.enums import (
    GroupSize,
    EventSize,
    InsuranceStatus,
    TemporaryVehicleInsuranceCoverageOption,
    TemporaryVehicleInsuranceOptionApi,
)


class GroupSizeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(GroupSize.choices, many=True)
        return Response(serializer.data)


class EventSizeViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(EventSize.choices, many=True)
        return Response(serializer.data)


class InsuranceStatusViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(InsuranceStatus.choices, many=True)
        return Response(serializer.data)


class TemporaryVehicleInsuranceCoverageOptionViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(TemporaryVehicleInsuranceCoverageOption.choices, many=True)
        return Response(serializer.data)


class TemporaryVehicleInsuranceOptionApiViewSet(viewsets.ViewSet):
    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumOutputSerializer})
    def list(self, request):
        serializer = EnumOutputSerializer(TemporaryVehicleInsuranceOptionApi.choices, many=True)
        return Response(serializer.data)
