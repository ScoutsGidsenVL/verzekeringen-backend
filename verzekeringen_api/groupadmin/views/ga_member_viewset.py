import logging
from typing import List

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema

from groupadmin.models import (
    ScoutsGroup,
    ScoutsGroupListResponse,
    ScoutsMember,
    ScoutsMemberListResponse,
    ScoutsMemberSearchResponse,
)
from groupadmin.serializers import (
    ScoutsMemberSerializer,
    ScoutsMemberFrontendSerializer,
    ScoutsMemberListResponseSerializer,
    ScoutsMemberSearchResponseSerializer,
)
from groupadmin.services import GroupAdmin
from groupadmin.utils import SettingsHelper


logger = logging.getLogger(__name__)


class ScoutsMemberView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberListResponseSerializer})
    @action(methods=["GET"], url_path="", detail=True)
    def view_member_list(self, request) -> Response:
        logger.debug("GA: Received request for member list")

        response: ScoutsMemberListResponse = self.service.get_member_list(request.user)

        serializer = ScoutsMemberListResponseSerializer(response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
    )
    def view_member_info_internal(self, request, group_admin_id: str) -> Response:
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member: ScoutsMember = self.service.get_member_info(request.user, group_admin_id)

        serializer = ScoutsMemberSerializer(member)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberFrontendSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
    )
    def view_member_info(self, request, group_admin_id: str) -> Response:
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member: ScoutsMember = self.service.get_member_info(request.user, group_admin_id)

        serializer = ScoutsMemberFrontendSerializer(member)

        return Response(serializer.to_representation(member))

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberListResponseSerializer})
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

        response: ScoutsMemberSearchResponse = self.service.search_member(request.user, term=term, group=group)

        serializer = ScoutsMemberSearchResponseSerializer(response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_member_profile_internal(self, request) -> Response:
        logger.debug("GA: Received request for current user profile")

        member: ScoutsMember = self.service.get_member_profile(request.user)

        serializer = ScoutsMemberSerializer(member)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberFrontendSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_member_profile(self, request) -> Response:
        logger.debug("GA: Received request for current user profile")

        member: ScoutsMember = self.service.get_member_profile(request.user)
        groups_response: ScoutsGroupListResponse = self.service.get_groups(request.user)

        member.groups = groups_response.groups

        known_admin_groups = SettingsHelper.get_administrator_groups()

        member_groups = [group.group_admin_id for group in member.groups]
        logger.debug("member groups: %s", member_groups)

        if any(group in member_groups for group in known_admin_groups):
            logger.debug("User is in known_admin_groups")

        serializer = ScoutsMemberFrontendSerializer(member)

        return Response(serializer.to_representation(member))
