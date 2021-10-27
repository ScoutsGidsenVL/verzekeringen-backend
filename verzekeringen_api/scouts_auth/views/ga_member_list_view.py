import logging
from typing import List

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import MemberList
from scouts_auth.serializers import MemberListSerializer
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberListView(views.APIView):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberListSerializer})
    @action(methods=["GET"], url_path="", detail=True, permissions_classes=perm_authenticated)
    def get(self, request):
        return self.view_member_list(request)

    def view_member_list(self, request) -> Response:
        logger.debug("GA: Received request for member list")

        members: List[MemberList] = self.service.get_member_list(request.user)

        serializer = MemberListSerializer(members)

        return Response(serializer.data)
