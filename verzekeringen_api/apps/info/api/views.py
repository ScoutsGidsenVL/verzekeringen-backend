from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from .serializers import InfoVariableOutputSerializer
from ..models import InfoVariable


class InfoVariableViewSet(viewsets.GenericViewSet):
    def get_queryset(self):
        return InfoVariable.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InfoVariableOutputSerializer})
    def retrieve(self, request, pk=None):
        info = self.get_object()
        serializer = InfoVariableOutputSerializer(info)

        return Response(serializer.data)
