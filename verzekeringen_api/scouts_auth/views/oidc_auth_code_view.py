from requests.exceptions import HTTPError

from rest_framework import views, permissions
from rest_framework.response import Response

from scouts_auth.services import OIDCService
from scouts_auth.serializers import (
    AuthCodeSerializer,
    TokenSerializer,
)
from scouts_auth.exceptions import TokenRequestException


class OIDCAuthCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]
    service = OIDCService()

    def post(self, request) -> Response:
        serializer = AuthCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = self.service.get_tokens_by_auth_code(
                auth_code=data.get("authCode"), redirect_uri=data.get("redirectUri")
            )
        except HTTPError as e:
            raise TokenRequestException(e)

        output_serializer = TokenSerializer(tokens)

        return Response(output_serializer.data)
