from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_insurances.info.models import InfoVariable
from scouts_insurances.info.serializers import InfoVariableSerializer


class InfoVariableViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InfoVariable.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InfoVariableSerializer})
    def retrieve(self, request, pk=None):
        info = self.get_object()
        serializer = InfoVariableSerializer(info)

        return Response(serializer.data)
