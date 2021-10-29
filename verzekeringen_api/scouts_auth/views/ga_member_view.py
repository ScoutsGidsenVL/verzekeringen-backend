import logging

from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import GroupAdminMember
from scouts_auth.serializers import GroupAdminMemberSerializer
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberView(views.APIView):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def get(self, request, group_admin_id: str):
        return self.view_member_info(request, group_admin_id)
    
    def view_member_info(self, request, group_admin_id: str):
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member_data: str = self.service.get_member_info(request.user, group_admin_id)
        logger.debug("DATA: %s", member_data)
        serializer = GroupAdminMemberSerializer(data=member_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.validated_data)
