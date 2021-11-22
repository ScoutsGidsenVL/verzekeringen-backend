import logging
from typing import List, Tuple

from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from groupadmin.models import ScoutsFunctionListResponse, ScoutsFunction
from groupadmin.serializers import ScoutsFunctionListResponseSerializer, ScoutsFunctionSerializer
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class ScoutsFunctionView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionListResponseSerializer})
    @action(
        methods=["GET"],
        url_path="",
        detail=False,
    )
    def view_functions(self, request) -> Response:
        logger.debug("GA: Received request for a list of all functions")

        functions_response: ScoutsFunctionListResponse = self.service.get_functions(request.user)
        serializer = ScoutsFunctionListResponseSerializer(functions_response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionListResponseSerializer})
    @action(
        methods=["GET"],
        url_path=r"group/(?P<group_group_admin_id_fragment>\w+)",
        detail=False,
    )
    def view_function_list(self, request, group_group_admin_id_fragment: str) -> Response:
        logger.debug(
            "GA: Received request for list of functions (group_group_admin_id_fragment: %s)",
            group_group_admin_id_fragment,
        )

        functions_response: ScoutsFunctionListResponse = self.service.get_functions(
            request.user, group_group_admin_id_fragment
        )

        serializer = ScoutsFunctionListResponseSerializer(functions_response)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsFunctionSerializer})
    @action(
        methods=["GET"],
        url_path=r"(?P<function_id>\w+)",
        detail=True,
    )
    def view_function(self, request, function_id: str) -> Response:
        logger.debug("GA: Received request for function info (function_id: %s)", function_id)

        function: ScoutsFunction = self.service.get_function(request.user, function_id)

        serializer = ScoutsFunctionSerializer(function)

        return Response(serializer.data)
