import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    GroupAdminMember,
)
from scouts_auth.serializers import (
    MemberSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberView(viewsets.GenericViewSet):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_info(self, request, group_admin_id: str):
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member: GroupAdminMember = self.service.get_member_info(request.user, group_admin_id)
