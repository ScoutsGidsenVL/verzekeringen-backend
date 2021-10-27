from typing import Tuple
from datetime import datetime

from scouts_auth.models import User, PartialScoutsGroup
from scouts_auth.util import SettingsHelper


class UserHelper:
    """
    Convenience class to parse user data coming from group admin into a User.

    @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html
    """

    def parse_claims(self, user: User, claims: dict) -> User:
        user.group_admin_id = claims.get("id", "")
        user.first_name = claims.get("vgagegevens", {}).get("voornaam", "")
        user.last_name = claims.get("vgagegevens", {}).get("achternaam", "")
        # The following aren't stored in database but are just put in memory
        try:
            raw_birth_date = claims.get("vgagegevens", {}).get("geboortedatum")
            user.birth_date = datetime.strptime(raw_birth_date, "%Y-%m-%d").date()
        except:
            pass
        user.phone_number = claims.get("persoonsgegevens", {}).get("gsm", "")
        user.membership_number = claims.get("verbondsgegevens", {}).get("lidnummer", "")
        user.roles = claims.get("functies", [])
        user.access_token = claims.get("access_token")

        return user

    def map_roles(
        self, scouts_user: User, claims: dict, roles=[], is_admin=False
    ) -> Tuple[User, list]:
        # Loop over active groups, check for admin and get more group info
        scouts_groups = [
            group_obj
            for group_obj in scouts_user.roles
            if not group_obj.get("einde", False)
        ]
        user_groups = []
        for group_obj in scouts_groups:
            group_id = group_obj.get("groep", "")
            href = next(
                link.get("href")
                for link in group_obj.get("links")
                if link.get("rel") == "groep" and link.get("method") == "GET"
            )
            user_groups.append(PartialScoutsGroup(identifier=group_id, href=href))

            if group_id in SettingsHelper.get_known_admin_groups():
                is_admin = True
                break

        scouts_user.partial_scouts_groups = user_groups

        # Check to see if the user is an admin after all
        if is_admin:
            roles.append("role_admin")

        return scouts_user, roles
