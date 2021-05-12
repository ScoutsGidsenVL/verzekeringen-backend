import requests
from django.conf import settings


def post_token_request(payload: dict) -> dict:
    response = requests.post(settings.OIDC_OP_TOKEN_ENDPOINT, data=payload)

    response.raise_for_status()

    return response.json()


def get_tokens_by_auth_code(auth_code: str, redirect_uri: str) -> dict:

    payload = {
        "code": auth_code,
        "grant_type": "authorization_code",
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "client_secret": settings.OIDC_RP_CLIENT_SECRET,
        "redirect_uri": redirect_uri,
    }

    return post_token_request(payload)


def get_tokens_by_refresh_token(refresh_token: str) -> dict:

    payload = {
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "client_id": settings.OIDC_RP_CLIENT_ID,
        "client_secret": settings.OIDC_RP_CLIENT_SECRET,
    }

    return post_token_request(payload)
