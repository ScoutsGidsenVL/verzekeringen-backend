import logging
from typing import List

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import GroupAdminMemberSearchResponse
from scouts_auth.serializers import (
    GroupAdminMemberSearchResponseSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminPartialMemberView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberSearchResponseSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<query>\w+)",
        detail=False,
    )
    def view_member_search(self, request, query: str):
        logger.debug("GA: Received request to search for members (query: %s)", query)

        members: List[GroupAdminMemberSearchResponse] = self.service.search_member(request.user, query)

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberSearchResponseSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<first_name>\w+)/(?P<last_name>\w+)",
        detail=False,
    )
    def view_member_similar_search(self, request, first_name: str, last_name: str):
        logger.debug(
            "GA: Received request to search for similar members (first_name: %s)(last_name: %s)", first_name, last_name
        )

        members: List[GroupAdminMemberSearchResponse] = self.service.search_similar_members(
            request.user, first_name, last_name
        )
