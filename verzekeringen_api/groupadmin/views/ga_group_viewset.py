import logging

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from groupadmin.models import ScoutsGroup, ScoutsGroupListResponse
from groupadmin.serializers import ScoutsGroupSerializer, ScoutsGroupListResponseSerializer
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class ScoutsGroupView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path="", detail=False)
    def view_groups(self, request):
        logger.debug("GA: Received request to view authorized groups")

        response_groups: ScoutsGroupListResponse = self.service.get_groups(request.user)
        groups = response_groups.groups

        serializer = ScoutsGroupSerializer(groups, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupListResponseSerializer})
    @action(methods=["GET"], url_path="", detail=False)
    def view_accountable_groups(self, request):
        logger.debug("GA: Received request for groups for which the authorized user is accountable (/vga call)")

        response_groups: ScoutsGroupListResponse = self.service.get_accountable_groups(request.user)
        groups = response_groups.groups

        serializer = ScoutsGroupListResponseSerializer(groups, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path=r"(?P<group_number>\w+)", detail=False)
    def view_group(self, request, group_number: str):
        logger.debug("GA: Received request for group info (group_number: %s)", group_number)

        group: ScoutsGroup = self.service.get_group(request.user, group_number)

        serializer = ScoutsGroupSerializer(group)

        return Response(serializer.data)
