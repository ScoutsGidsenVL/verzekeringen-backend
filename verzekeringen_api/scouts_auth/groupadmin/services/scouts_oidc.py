import logging

from django.conf import settings

from scouts_auth.auth.oidc import InuitsOIDCAuthenticationBackend

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.serializers import AbstractScoutsMemberSerializer
from scouts_auth.groupadmin.services import GroupAdmin, ScoutsAuthorizationService


logger = logging.getLogger(__name__)


class ScoutsOIDCAuthenticationBackend(InuitsOIDCAuthenticationBackend):
    service = GroupAdmin()
    authorization_service = ScoutsAuthorizationService()

    def get_userinfo(self, access_token, id_token, payload) -> dict:
        """
        Return user details dictionary. The id_token and payload are not used
        in the default implementation, but may be used when overriding
        this method.
        """
        result = super().get_userinfo(access_token, id_token, payload)

        return result

    def get_or_create_user(self, access_token, id_token, payload):
        """Returns a User instance if 1 user is found. Creates a user if not found
        and configured to do so. Returns nothing if multiple users are matched."""
        user_info = self.get_userinfo(access_token, id_token, payload)

        claims_verified = self.verify_claims(user_info)
        if not claims_verified:
            msg = "Claims verification failed"
            raise ValidationError(msg)

        # email based filtering
        users = self.filter_users_by_claims(user_info)

        logger.debug("GET OR CREATE USER FOUND %d user(s)", len(users))

        if len(users) == 1:
            return self.update_user(users[0], user_info)
        elif len(users) > 1:
            # In the rare case that two user accounts have the same email address,
            # bail. Randomly selecting one seems really wrong.
            msg = "Multiple users returned"
            raise ValidationError(msg)
        elif self.get_settings("OIDC_CREATE_USER", True):
            user = self.create_user(user_info)
            return user
        else:
            logger.debug(
                "Login failed: No user with %s found, and " "OIDC_CREATE_USER is False",
                self.describe_user_by_claims(user_info),
            )
            return None
    
    def filter_users_by_claims(self, claims):
        """Return all users matching the group admin id."""
        # logger.debug("CLAIMS: %s", claims)
        group_admin_id = claims.get("id")
        if not group_admin_id:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(group_admin_id=group_admin_id)
    
    def create_user(self, claims: dict) -> settings.AUTH_USER_MODEL:
        """
        Create and return a new user object.
        """
        username = None
        access_token = claims.get("access_token", None)
        if access_token:
            try:
                decoded = jwt.decode(
                    access_token,
                    algorithms=["RS256"],
                    verify=False,
                    options={"verify_signature": False},
                )
                username = decoded.get("preferred_username", None)
            except:
                logger.error("Unable to decode JWT token - Do you need a refresh ?")
        username = username if username else member.username
        # logger.debug("USER: create user %s", username)

        member: AbstractScoutsMember = self._load_member_data(data=claims)
        user: settings.AUTH_USER_MODEL = self.UserModel.objects.create_user(
            id=member.group_admin_id, username=username, email=member.email
        )
        user = self._merge_member_data(user, member, claims)

        logger.info(
            "SCOUTS OIDC AUTHENTICATION: Created user from group admin member %s",
            member.group_admin_id,
            user=user,
        )
        self.scouts_user_service.handle_oidc_login(user=user)

        return user

    def update_user(
        self, user: settings.AUTH_USER_MODEL, claims: dict
    ) -> settings.AUTH_USER_MODEL:
        """
        Update existing user with new claims if necessary, save, and return the updated user object.
        """
        # logger.debug("USER: update user")

        member: AbstractScoutsMember = self._load_member_data(data=claims)
        user: settings.AUTH_USER_MODEL = self._merge_member_data(user, member, claims)

        logger.info(
            "SCOUTS OIDC AUTHENTICATION: Updated user: %s",
            user
        )

        return user

    def _load_member_data(self, data: dict) -> AbstractScoutsMember:
        serializer = AbstractScoutsMemberSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        member: AbstractScoutsMember = serializer.save()

        return member

    def _merge_member_data(
        self, user: settings.AUTH_USER_MODEL, member: AbstractScoutsMember, claims: dict
    ) -> settings.AUTH_USER_MODEL:
        user.group_admin_id = member.group_admin_id
        user.gender = member.personal_data.gender
        user.phone_number = member.personal_data.phone_number
        user.membership_number = member.scouts_data.membership_number
        user.customer_number = member.scouts_data.customer_number
        user.birth_date = member.group_admin_data.birth_date
        user.first_name = member.group_admin_data.first_name
        user.last_name = member.group_admin_data.last_name
        user.email = member.email

        user.scouts_groups = member.scouts_groups
        user.addresses = member.addresses
        user.functions = member.functions
        user.group_specific_fields = member.group_specific_fields
        user.links = member.links

        user.access_token = claims.get("access_token")
        user = self.map_user_with_claims(user)

        user.full_clean()
        user.save()

        return user


    def map_user_with_claims(
        self, user: settings.AUTH_USER_MODEL, claims: dict = None
    ) -> settings.AUTH_USER_MODEL:
        """
        Override the mapping in InuitsOIDCAuthenticationBackend to handle scouts-specific data.
        """
        logger.debug("SCOUTS OIDC AUTHENTICATION: mapping user claims", user=user)
        return self.authorization_service.update_user_authorizations(user=user)
