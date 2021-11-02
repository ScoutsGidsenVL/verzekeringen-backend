import logging

from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import GroupAdminMember, MemberList
from scouts_auth.serializers import MemberListSerializer, GroupAdminMemberSerializer
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberListSerializer})
    @action(methods=["GET"], url_path="", detail=True, permissions_classes=perm_authenticated)
    def view_member_list(self, request) -> Response:
        logger.debug("GA: Received request for member list")

        member_list: MemberList = self.service.get_member_list(request.user)

        serializer = MemberListSerializer(member_list)

        logger.debug("member list: %s", member_list)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_info(self, request, group_admin_id: str):
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member: GroupAdminMember = self.service.get_member_info(request.user, group_admin_id)
        logger.debug("MEMBER: %s", str(member))

        serializer = GroupAdminMemberSerializer(member)
        logger.debug("HIER")
        logger.debug("MEMBER: %s", str(member))

        return Response(serializer.data)
