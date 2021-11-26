from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.insurances.models.enums import GroupSize

from inuits.serializers import EnumSerializer


class GroupSizeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        serializer = EnumSerializer(GroupSize.choices, many=True)
        return Response(serializer.data)
