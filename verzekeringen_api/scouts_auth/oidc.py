import requests, logging
from requests.exceptions import HTTPError

from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group

from rest_framework import exceptions

from scouts_auth.auth.models import User
from scouts_auth.auth.utils import SettingsHelper
from scouts_auth.auth.signals import ScoutsAuthSignalSender


logger = logging.getLogger(__name__)


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def get_userinfo(self, access_token, id_token, payload) -> dict:
        """
        Return user details dictionary. The id_token and payload are not used
        in the default implementation, but may be used when overriding
        this method.
        """

        logger.debug(
            "User info requested with access_token %s, " + ", id_token %s and payload %s",
            access_token,
            id_token,
            payload,
        )

        user_response = requests.get(
            SettingsHelper.get_oidc_op_user_endpoint(),
            headers={"Authorization": "Bearer {0}".format(access_token)},
            verify=self.get_settings("OIDC_VERIFY_SSL", True),
            timeout=self.get_settings("OIDC_TIMEOUT", None),
            proxies=self.get_settings("OIDC_PROXY", None),
        )
        user_response.raise_for_status()
        result = user_response.json()

        # Add token to user response so we can access it later
        result["access_token"] = access_token

        return result

    def create_user(self, claims: dict) -> User:
        """
        Create and return a new user object.
        """
        email = claims.get("email")
        username = self.get_username(claims)

        user = self.UserModel.objects.create_user(username, email)

        user.full_clean()
        user.save()

        return user

    def update_user(self, user: User, claims: dict) -> User:
        """
        Update existing user with new claims if necessary,
        save, and return the updated user object.
        """
        user.full_clean()
        user.save()

        return user

    def map_user_with_claims(self, user: User, claims: dict):
        """
        Maps the user to authorized user roles with the provided claims.
        """
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)

        logger.debug("Mapping user %s %s with local claims", user.first_name, user.last_name)

        roles = claims.get(settings.OIDC_RP_CLIENT_ID, {}).get("roles", [])
        user = self.map_user_roles(user, roles)

        return user

    def map_user_roles(self, user: User, claim_roles):
        # First clear all groups from user and set superuser false
        user.is_superuser = False
        user.groups.clear()
        for role in claim_roles:
            try:
                group = Group.objects.get(name=role)
                user.groups.add(group)
                # Set user super admin if role is super_admin
                if group.name == "role_super_admin":
                    user.is_superuser = True
            except ObjectDoesNotExist:
                pass

        return user


class InuitsOIDCAuthentication(OIDCAuthentication):
    def authenticate(self, request):
        """ "
        Call parent authenticate but catch HTTPError 401 always,
        even without www-authenticate.
        """

        try:
            logger.debug("Authenticating user with OIDC backend")

            result = super().authenticate(request)

            if result is None:
                logger.error("SCOUTS-AUTH: Authentication failed")

                return None

            if isinstance(result, tuple):
                (user, token) = result

                ScoutsAuthSignalSender().send_authenticated(user)

            return result
        except HTTPError as exc:
            logging.exception("SCOUTS-AUTH: Authentication error: %s", exc.response.json())

            response = exc.response
            # If oidc returns 401 return auth failed error
            if response.status_code == 401:
                logging.error("SCOUTS-AUTH: 401 Unable to authenticate")

                raise exceptions.AuthenticationFailed(response.json().get("error_description", response.text))

            raise
