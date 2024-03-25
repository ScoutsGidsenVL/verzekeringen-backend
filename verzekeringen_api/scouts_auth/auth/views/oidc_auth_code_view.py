import logging

from drf_yasg.utils import swagger_auto_schema
from requests.exceptions import HTTPError
from rest_framework import permissions, status, views
from rest_framework.response import Response

from scouts_auth.auth.exceptions import TokenRequestException
from scouts_auth.auth.serializers import AuthCodeSerializer, TokenSerializer
from scouts_auth.auth.services import OIDCService

logger = logging.getLogger(__name__)


class OIDCAuthCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]
    service = OIDCService()

    @swagger_auto_schema(
        request_body=AuthCodeSerializer,
        responses={status.HTTP_202_ACCEPTED: TokenSerializer},
    )
    def post(self, request) -> Response:
        serializer = AuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = self.service.get_tokens_by_auth_code(
                auth_code=data.get("authCode"), redirect_uri=data.get("redirectUri")
            )
        except HTTPError as exc:
            logger.error(f"Failed to refresh tokens: {exc}")
            raise TokenRequestException("Failed to refresh tokens.")

        output_serializer = TokenSerializer(tokens)

        return Response(output_serializer.data)
