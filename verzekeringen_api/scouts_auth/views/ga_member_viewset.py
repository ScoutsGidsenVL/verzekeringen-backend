import logging

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    GroupAdminMember,
    GroupAdminMemberListResponse,
    GroupAdminMemberSearchResponse,
)
from scouts_auth.serializers import (
    GroupAdminMemberSerializer,
    GroupAdminMemberListResponseSerializer,
    GroupAdminMemberSearchResponseSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberListResponseSerializer})
    @action(methods=["GET"], url_path="", detail=True)
    def view_member_list(self, request) -> Response:
        logger.debug("GA: Received request for member list")

        response: GroupAdminMemberListResponse = self.service.get_member_list(request.user)

        serializer = GroupAdminMemberListResponseSerializer(response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberListResponseSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?:/(?P<term>\w+))?(?:/(?P<group>\w+))?",
        detail=True,
    )
    def search_members(self, request, term: str, group: str = None) -> Response:
        logger.debug("GA: Received request to search for members")
        logger.debug(
            "GA: Member search parameters: term(%s) - group(%s)", term if term else "", group if group else ""
        )

        if not term:
            raise ValidationError("Url param 'term' is a required filter")

        response: GroupAdminMemberSearchResponse = self.service.search_member(request.user, term=term, group=group)

        serializer = GroupAdminMemberSearchResponseSerializer(response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
    )
    def view_member_info(self, request, group_admin_id: str) -> Response:
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member: GroupAdminMember = self.service.get_member_info(request.user, group_admin_id)

        serializer = GroupAdminMemberSerializer(member)

        return Response(serializer.data)
