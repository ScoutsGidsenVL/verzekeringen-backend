from rest_framework import views, permissions
from rest_framework.response import Response
from requests.exceptions import HTTPError

from scouts_auth.services import OIDCService
from scouts_auth.serializers import (
    RefreshSerializer,
    TokenSerializer,
)
from scouts_auth.exceptions import TokenRequestException


class OIDCRefreshView(views.APIView):
    permission_classes = [permissions.AllowAny]
    service = OIDCService()

    def post(self, request):
        serializer = RefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = self.service.get_tokens_by_refresh_token(
                refresh_token=data.get("refreshToken")
            )
        except HTTPError as e:
            raise TokenRequestException(e)

        output_serializer = TokenSerializer(tokens)

        return Response(output_serializer.data)
