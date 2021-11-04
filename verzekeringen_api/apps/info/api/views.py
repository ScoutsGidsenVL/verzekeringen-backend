from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.info.api.serializers import InfoVariableOutputSerializer
from apps.info.models import InfoVariable


class InfoVariableViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InfoVariable.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InfoVariableOutputSerializer})
    def retrieve(self, request, pk=None):
        info = self.get_object()
        serializer = InfoVariableOutputSerializer(info)

        return Response(serializer.data)
