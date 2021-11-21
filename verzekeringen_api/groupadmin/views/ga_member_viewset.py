import logging
from typing import List

from django.conf import settings

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema

from groupadmin.models import (
    ScoutsGroupListResponse,
    ScoutsMember,
    ScoutsMemberListResponse,
)
from groupadmin.serializers import (
    ScoutsMemberSerializer,
    ScoutsMemberFrontendSerializer,
    ScoutsMemberSearchFrontendSerializer,
    ScoutsMemberListResponseSerializer,
    ScoutsUserSerializer,
)
from groupadmin.services import GroupAdminMemberService


logger = logging.getLogger(__name__)


class ScoutsMemberView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdminMemberService()

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
        url_path=r"(?:/(?P<term>\w+))?(?:/(?P<group_group_admin_id>\w+))?",
        detail=True,
    )
    def search_members(self, request, term: str, group_group_admin_id: str = None) -> Response:
        logger.debug("GA: Received request to search for members")
        logger.debug(
            "GA: Member search parameters: term(%s) - group_group_admin_id(%s)",
            term if term else "",
            group_group_admin_id if group_group_admin_id else "",
        )

        if not term:
            raise ValidationError("Url param 'term' is a required filter")

        results: List[ScoutsMember] = self.service.search_member_filtered(
            request.user, term=term, group_group_admin_id=group_group_admin_id
        )

        serializer = ScoutsMemberSearchFrontendSerializer(results, many=True)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_member_profile_internal(self, request) -> Response:
        logger.debug("GA: Received request for current user GA member profile")

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
        logger.debug("GA: Received request for current user GA member profile")

        member: ScoutsMember = self.service.get_member_profile(request.user)
        groups_response: ScoutsGroupListResponse = self.service.get_groups(request.user)

        member.groups = groups_response.groups

        serializer = ScoutsMemberFrontendSerializer(member)

        return Response(serializer.to_representation(member))

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberFrontendSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=True,
    )
    def view_user(self, request) -> Response:
        logger.debug("GA: Received request for current user profile")

        user: settings.AUTH_USER_MODEL = request.user

        serializer = ScoutsUserSerializer(user)

        return Response(serializer.data)