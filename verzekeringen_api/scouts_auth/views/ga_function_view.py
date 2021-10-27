import logging
from typing import List

from rest_framework import status, views
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import (
    ScoutsFunction,
)
from scouts_auth.serializers import (
    ScoutsFunctionSerializer,
)
from scouts_auth.services import GroupAdmin


logger = logging.getLogger(__name__)


class GroupAdminFunctionView(views.APIView):

    perm_authenticated = [IsAuthenticated]
    service = GroupAdmin()

    @classmethod
    def get_extra_actions(cls):
        return []

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionSerializer})
    @action(
        methods=["GET"],
        url_path=r"group/(?P<group_number_fragment>\w+)",
        detail=False,
        permissions_classes=perm_authenticated,
    )
    def view_functions(self, request, group_number_fragment: str):
        logger.debug("GA: Received request for list of functions (group_number_fragment: %s)", group_number_fragment)

        functions: List[ScoutsFunction] = self.service.get_functions(request.user, group_number_fragment)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<function_id>\w+)",
        detail=True,
        permissions_classes=perm_authenticated,
    )
    def view_function(self, request, function_id: str):
        logger.debug("GA: Received request for function info (function_id: %s)", function_id)

        function: ScoutsFunction = self.service.get_function(request.user, function_id)
