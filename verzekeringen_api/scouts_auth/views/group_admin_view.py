import logging

from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    GroupAdminMember,
    MemberMedicalFlashCard,
)
from scouts_auth.serializers import (
    MemberSerializer,
    MemberMedicalFlashCardSerializer,
    ScoutsGroupSerializer,
    ScoutsFunctionSerializer,
    MemberListMemberSerializer,
    PartialScoutsUserSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminView(views.APIView):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberSerializer})
    @action(
        methods=["GET"],
        url_path=r"member/(?P<group_admin_id>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_info(self, request, group_admin_id: str):
        logger.debug("GA: Received request for member info (group_admin_id: %s)", group_admin_id)

        member: GroupAdminMember = self.service.get_member_info(request.user, group_admin_id)

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberMedicalFlashCardSerializer})
    @action(
        methods=["GET"],
        url_path=r"flash_card/(?P<group_admin_id>\w+)",
        detail=True,
        permissions_classes=perm_authenticated,
    )
    def view_member_medical_flash_card(self, request, group_admin_id: str):
        logger.debug("GA: Received request for member medical flash card (group_admin_id: %s)", group_admin_id)

        card: MemberMedicalFlashCard = self.service.get_member_medical_flash_card(request.user, group_admin_id)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path="groups", detail=False, permissions_classes=perm_authenticated)
    def view_groups(self, request):
        logger.debug("GA: Received request to view authorized groups")

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(methods=["GET"], url_path="groups/vga", detail=False, permissions_classes=perm_authenticated)
    def view_accountable_groups(self, request):
        logger.debug("GA: Received request for groups for which the authorized user is accountable (VGA call)")

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsGroupSerializer})
    @action(
        methods=["GET"], url_path=r"groups/(?P<group_number>\w+)", detail=True, permissions_classes=perm_authenticated
    )
    def view_group(self, request, group_number: str):
        logger.debug("GA: Received request for group info (group_number: %s)", group_number)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionSerializer})
    @action(
        methods=["GET"],
        url_path=r"functions/group/(?P<group_number_fragment>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_functions(self, request, group_number_fragment: str):
        logger.debug("GA: Received request for list of functions (group_number_fragment: %s)", group_number_fragment)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionSerializer})
    @action(
        methods=["GET"],
        url_path=r"functions/(?P<function_id>\w+)",
        detail=True,
        permissions_classes=perm_authenticated,
    )
    def view_function(self, request, function_id: str):
        logger.debug("GA: Received request for function info (function_id: %s)", function_id)

    @swagger_auto_schema(responses={status.HTTP_200_OK: MemberListMemberSerializer})
    @action(methods=["GET"], url_path="members/list", detail=False, permissions_classes=perm_authenticated)
    def view_member_list(self, request):
        logger.debug("GA: Received request for member list")

    @swagger_auto_schema(responses={status.HTTP_200_OK: PartialScoutsUserSerializer})
    @action(
        methods=["GET"],
        url_path=r"members/search/(?P<query>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_search(self, request, query: str):
        logger.debug("GA: Received request to search for members (query: %s)", query)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PartialScoutsUserSerializer})
    @action(
        methods=["GET"],
        url_path=r"members/search/(?P<first_name>\w+)/(?P<last_name>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_member_similar_search(self, request, first_name: str, last_name: str):
        logger.debug(
            "GA: Received request to search for similar members (first_name: %s)(last_name: %s)", first_name, last_name
        )
