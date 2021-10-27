import logging, requests

from django.conf import settings

from scouts_auth.util import SettingsHelper


logger = logging.getLogger(__name__)


class OIDCService:

    oidc_endpoint = SettingsHelper.get_oidc_op_token_endpoint()
    oidc_rp_client_id = SettingsHelper.get_oidc_rp_client_id()
    oidc_rp_client_secret = SettingsHelper.get_oidc_rp_client_secret()

    def _post_token_request(self, payload: dict) -> dict:
        response = requests.post(self.oidc_endpoint, data=payload)

        response.raise_for_status()

        return response.json()

    def get_tokens_by_auth_code(self, auth_code: str, redirect_uri: str) -> dict:
        payload = {
            "code": auth_code,
            "grant_type": "authorization_code",
            "client_id": self.oidc_rp_client_id,
            "client_secret": self.oidc_rp_client_secret,
            "redirect_uri": redirect_uri,
        }
        logger.debug("SCOUTS_AUTH: OIDC - sending authentication token")
        return self._post_token_request(payload)

    def get_tokens_by_refresh_token(self, refresh_token: str) -> dict:
        payload = {
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.oidc_rp_client_id,
            "client_secret": self.oidc_rp_client_secret,
        }
        logger.debug("SCOUTS_AUTH: OIDC - refreshing authentication")
        return self._post_token_request(payload)
