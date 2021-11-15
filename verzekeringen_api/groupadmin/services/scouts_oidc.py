import logging

from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist

from scouts_auth.oidc import InuitsOIDCAuthenticationBackend

from groupadmin.models import ScoutsUser, ScoutsMember, ScoutsGroup, ScoutsFunction
from groupadmin.serializers import ScoutsMemberSerializer
from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class ScoutsOIDCAuthenticationBackend(InuitsOIDCAuthenticationBackend):
    service = GroupAdmin()

    def create_user(self, claims: dict) -> ScoutsUser:
        """
        Create and return a new user object.
        """
        member: ScoutsMember = self.load_member_data(data=claims)
        user: ScoutsUser = self.UserModel.objects.create_user(username=member.username, email=member.email)
        user = self.merge_member_data(user, member, claims)

        return user

    def update_user(self, user: ScoutsUser, claims: dict) -> ScoutsUser:
        """
        Update existing user with new claims if necessary, save, and return the updated user object.
        """
        member: ScoutsMember = self.load_member_data(data=claims)
        user: ScoutsUser = self.merge_member_data(user, member, claims)

        return user

    def load_member_data(self, data: dict) -> ScoutsMember:
        serializer = ScoutsMemberSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        member: ScoutsMember = serializer.save()

        return member

    def merge_member_data(self, user: ScoutsUser, member: ScoutsMember, claims: dict) -> ScoutsUser:
        user.group_admin_id = member.group_admin_id
        user.gender = member.personal_data.gender
        user.phone = member.personal_data.phone
        user.membership_number = member.scouts_data.membership_number
        user.customer_number = member.scouts_data.customer_number
        user.birth_date = member.group_admin_data.birth_date
        user.first_name = member.group_admin_data.first_name
        user.last_name = member.group_admin_data.last_name
        user.email = member.email

        user.scouts_groups = member.groups
        user.addresses = member.addresses
        user.functions = member.functions
        user.group_specific_fields = member.group_specific_fields
        user.links = member.links

        user.access_token = claims.get("access_token")
        user = self.map_user_with_claims(user, member)

        user.full_clean()
        user.save()

        return user

    def map_user_with_claims(self, user: ScoutsUser, member: ScoutsMember):
        """
        Override the mapping in InuitsOIDCAuthenticationBackend to handle scouts-specific data.
        """
        # Everybody gets role user and assume the user is not an admin
        roles = ["role_user"]
        # ROLE: role_leader -> The user is a leader
        role_leader = "role_leader"
        # ROLE: role_group_leader -> The user is a group leader
        role_group_leader = "role_group_leader"
        # ROLE: role_administrator -> The user belongs to an administrative group
        role_administrator = "role_administrator"

        if user.is_administrator:
            roles.append(role_administrator)

        user = self.map_user_roles(user, roles)

        return user

    def map_user_roles(self, user: ScoutsUser, claim_roles):
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
