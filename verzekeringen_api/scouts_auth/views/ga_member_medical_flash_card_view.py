import logging

from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    MemberMedicalFlashCard,
)
from scouts_auth.serializers import (
    MemberMedicalFlashCardSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminMemberMedicalFlashCardView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberMedicalFlashCardSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<group_admin_id>\w+)",
        detail=True,
    )
    def view_member_medical_flash_card(self, request, group_admin_id: str):
        logger.debug("GA: Received request for member medical flash card (group_admin_id: %s)", group_admin_id)

        card: MemberMedicalFlashCard = self.service.get_member_medical_flash_card(request.user, group_admin_id)
