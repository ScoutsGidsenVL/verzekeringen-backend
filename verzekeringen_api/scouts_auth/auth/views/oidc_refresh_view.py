import logging

from requests.exceptions import HTTPError

from rest_framework import status, views, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.auth.services import OIDCService
from scouts_auth.auth.serializers import (
    RefreshSerializer,
    TokenSerializer,
)
from scouts_auth.auth.exceptions import TokenRequestException


logger = logging.getLogger(__name__)


class OIDCRefreshView(views.APIView):
    permission_classes = [permissions.AllowAny]
    service = OIDCService()

    @swagger_auto_schema(
        request_body=RefreshSerializer,
        responses={status.HTTP_202_ACCEPTED: TokenSerializer},
    )
    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = self.service.get_tokens_by_refresh_token(
                user=request.user, refresh_token=data.get("refreshToken")
            )
        except HTTPError as exc:
            logger.error("Failed to refresh tokens: {exc}")
            raise TokenRequestException("Failed to refresh tokens.")

        output_serializer = TokenSerializer(tokens)

        return Response(output_serializer.data)
