import logging

from rest_framework import views, permissions, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import User
from scouts_auth.serializers import UserSerializer


logger = logging.getLogger(__name__)


class CurrentUserView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer})
    def get(self, request):
        try:
            user: User = request.user

            logger.debug("USER: %s", user)

            user.fetch_detailed_group_info()
            serializer = UserSerializer(request.user)

            return Response(serializer.data)
        except Exception as exc:
            logger.error("SCOUTS_AUTH: Error while performing the me call", exc)
