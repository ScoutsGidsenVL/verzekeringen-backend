from rest_framework import views, status, permissions
from rest_framework.response import Response
from requests.exceptions import HTTPError
from .serializers import AuthCodeInputSerializer, RefreshInputSerializer, TokenOutputSerializer
from ..services.token_request_service import get_tokens_by_auth_code, get_tokens_by_refresh_token
from ..exceptions import TokenRequestException


class AuthCodeView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = AuthCodeInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = get_tokens_by_auth_code(auth_code=data.get("authCode"), redirect_uri=data.get("redirectUri"))
        except HTTPError as e:
            raise TokenRequestException(e)

        output_serializer = TokenOutputSerializer(tokens)

        return Response(output_serializer.data)


class RefreshView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RefreshInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        try:
            tokens = get_tokens_by_refresh_token(refresh_token=data.get("refreshToken"))
        except HTTPError as e:
            raise TokenRequestException(e)

        output_serializer = TokenOutputSerializer(tokens)

        return Response(output_serializer.data)
