import logging
from typing import List

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    ScoutsGroup,
)
from scouts_auth.serializers import (
    ScoutsGroupSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminGroupView(views.APIView):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path="", detail=False, permissions_classes=perm_authenticated)
    def get(self, request):
        return self.view_groups(request)

    def view_groups(self, request):
        logger.debug("GA: Received request to view authorized groups")

        groups: List[ScoutsGroup] = self.service.get_groups(request.user)

        serializer = ScoutsGroupSerializer(groups)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path="vga", detail=False, permissions_classes=perm_authenticated)
    def view_accountable_groups(self, request):
        logger.debug("GA: Received request for groups for which the authorized user is accountable (VGA call)")

        groups: List[ScoutsGroup] = self.service.get_accountable_groups(request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path=r"(?P<group_number>\w+)", detail=True, permissions_classes=perm_authenticated)
    def view_group(self, request, group_number: str):
        logger.debug("GA: Received request for group info (group_number: %s)", group_number)

        group: ScoutsGroup = self.service.get_group(request.user, group_number)
