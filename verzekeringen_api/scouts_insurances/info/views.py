from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

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
