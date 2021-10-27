import logging
from typing import List

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    PartialScoutsUser,
)
from scouts_auth.serializers import (
    PartialScoutsUserSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminPartialMemberView(viewsets.GenericViewSet):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: PartialScoutsUserSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<query>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_search(self, request, query: str):
        logger.debug("GA: Received request to search for members (query: %s)", query)

        members: List[PartialScoutsUser] = self.service.search_member(request.user, query)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PartialScoutsUserSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<first_name>\w+)/(?P<last_name>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_similar_search(self, request, first_name: str, last_name: str):
        logger.debug(
            "GA: Received request to search for similar members (first_name: %s)(last_name: %s)", first_name, last_name
        )

        members: List[PartialScoutsUser] = self.service.search_similar_members(request.user, first_name, last_name)
