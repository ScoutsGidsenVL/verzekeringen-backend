import logging
from typing import List

from django.http import HttpResponse
from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import ScoutsGroup, User
from scouts_auth.serializers import ScoutsGroupSerializer, UserSerializer
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer})
    def get(self, request):
        try:
            user: User = request.user

            logger.debug("USER: %s", user.username)

            group_data = self.service.get_groups(request.user)
            group_serializer = ScoutsGroupSerializer(data=group_data.get("groepen", []))
            group_serializer.is_valid(raise_exception=True)

            groups: List[ScoutsGroup] = group_serializer.validated_data
            user.groups.set(groups)

            serializer = UserSerializer(request.user)
            data = serializer.data

            if data:
                return Response(data)
            
            return HttpResponse(status=204)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while performing the me call", exc)
