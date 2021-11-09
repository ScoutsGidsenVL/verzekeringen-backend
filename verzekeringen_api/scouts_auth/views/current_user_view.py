import logging
from typing import List

from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import User
from scouts_auth.serializers import UserSerializer


from groupadmin.models import ScoutsGroup
from groupadmin.serializers import ScoutsGroupSerializer
from groupadmin.services import GroupAdmin


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
            group_serializer = ScoutsGroupSerializer(data=group_data, many=True)
            group_serializer.is_valid(raise_exception=True)

            groups: List[ScoutsGroup] = group_serializer.validated_data
            user.scouts_groups = groups

            serializer = UserSerializer(request.user)
            data = serializer.data

            return Response(data)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while performing the me call", exc)
