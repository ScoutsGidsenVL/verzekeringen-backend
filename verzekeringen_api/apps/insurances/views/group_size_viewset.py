from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_insurances.insurances.models.enums import GroupSize


class GroupSizeViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: EnumSerializer})
    def list(self, request):
        serializer = EnumSerializer(GroupSize.choices, many=True)
        return Response(serializer.data)
