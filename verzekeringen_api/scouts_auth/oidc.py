import requests, logging
from mozilla_django_oidc.auth import OIDCAuthenticationBackend
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import Group
from rest_framework import exceptions
from requests.exceptions import HTTPError

from scouts_auth.models import UserHelper
from scouts_auth.utils import SettingsHelper


logger = logging.getLogger(__name__)


class InuitsOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    def get_userinfo(self, access_token, id_token, payload):
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

    def create_user(self, claims):
        """
        Create and return a new user object.
        """

        email = claims.get("email")
        username = self.get_username(claims)

        # Creating user like this because user is special
        user = self.UserModel.objects.create_user(username, email)
        # Then update user fields with claims
        user.full_clean()
        user.save()

        return user

    def update_user(self, user, claims):
        """
        Update existing user with new claims if necessary,
        save, and return the updated user object.
        """

        updated_user = self.map_user_with_claims(user, claims)
        updated_user.full_clean()
        updated_user.save()

        return updated_user

    def map_user_with_claims(self, user, claims):
        """
        Maps the user to authorized user roles with the provided claims.

        If the source of the claims is the scouts group admin website,
        redirect to map_user_with_scouts_claims, otherwise redirect to
        map_user_with_userinfo_claims.
        """

        if settings.OIDC_OP_USER_ENDPOINT.startswith("https://groepsadmin.scoutsengidsenvlaanderen.be"):
            return self.map_user_with_scouts_claims(user, claims)
        else:
            return self.map_user_with_userinfo_claims(user, claims)

    def map_user_with_userinfo_claims(self, user, claims):
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)

        logger.debug("Mapping user %s %s with local claims", user.first_name, user.last_name)

        roles = claims.get(settings.OIDC_RP_CLIENT_ID, {}).get("roles", [])
        user = self.map_user_roles(user, roles)

        return user

    def map_user_with_scouts_claims(self, user, claims):
        logger.debug("Mapping user %s %s with scouts claims", user.first_name, user.last_name)

        helper = UserHelper()

        # Process the data coming from group admin
        user = helper.parse_claims(user, claims)
        # Everybody gets role user and assume the user is not an admin
        roles = ["role_user"]
        is_admin = False
        user, roles = helper.map_roles(user, claims, roles, is_admin)

        user = self.map_user_roles(user, roles)

        return user

    def map_user_roles(self, user, claim_roles):
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

            (user, token) = result

            logger.debug("USER: %s", user)
            logger.debug("USER: %s", dir(user))

            return result
        except HTTPError as exc:
            logging.exception("SCOUTS-AUTH: Authentication error: %s", exc.response.json())

            response = exc.response
            # If oidc returns 401 return auth failed error
            if response.status_code == 401:
                logging.error("SCOUTS-AUTH: 401 Unable to authenticate")

                raise exceptions.AuthenticationFailed(response.json().get("error_description", response.text))

            raise
