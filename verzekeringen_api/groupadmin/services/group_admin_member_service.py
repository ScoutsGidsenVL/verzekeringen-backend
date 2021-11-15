import requests, logging
from typing import List
from datetime import date, datetime, timedelta

from groupadmin.models import ScoutsAddress, ScoutsMember, PostcodeCity
from scouts_auth.utils import SettingsHelper


logger = logging.getLogger(__name__)


class GroupAdminMemberService:
    def _get_group_admin_member_detail_data(
        self, active_user: SettingsHelper.get_auth_user_model(), group_admin_id: str
    ) -> dict:
        """
            Makes call to IDP to retrieve member details.

        Args:
            active_user (scouts_auth.User): settings.AUTH_USER_MODEL
            group_admin_id (str): foreign id

        Returns: GroupAdminMember
        """
        response = requests.get(
            "{0}/{1}".format(SettingsHelper.get_group_admin_member_detail_endpoint(), group_admin_id),
            headers={"Authorization": "Bearer {0}".format(active_user.access_token)},
        )

        response.raise_for_status()

        return response.json()

    def _parse_member_data(self, member_data: dict, group_admin_id: str) -> ScoutsMember:
        try:
            birth_date_str = member_data.get("vgagegevens").get("geboortedatum")
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except:
            birth_date = None

        addresses = member_data.get("adressen", [])
        if len(addresses) == 0:
            raise Exception("Something went wrong, chosen member has no address")
        raw_address = addresses[0]
        postcode_city = PostcodeCity(postcode=raw_address.get("postcode"), name=raw_address.get("gemeente"))

        address = ScoutsAddress(
            street=raw_address.get("straat"),
            number=raw_address.get("nummer"),
            letter_box=raw_address.get("bus", ""),
            postcode_city=postcode_city,
        )

        member = ScoutsMember(
            first_name=member_data.get("vgagegevens", {}).get("voornaam"),
            last_name=member_data.get("vgagegevens", {}).get("achternaam"),
            gender=member_data.get("persoonsgegevens", {}).get("geslacht"),
            email=member_data.get("email"),
            birth_date=birth_date,
            phone_number=member_data.get("persoonsgegevens", {}).get("gsm", ""),
            group_admin_id=group_admin_id,
            membership_number=member_data.get("verbondsgegevens", {}).get("lidnummer", ""),
            addresses=[address],
        )

        logger.debug(
            "Detailed member data for id %s: %s %s",
            group_admin_id,
            member.first_name,
            member.last_name,
        )

        return member

    def group_admin_member_detail(
        self, active_user: SettingsHelper.get_auth_user_model(), group_admin_id: str
    ) -> ScoutsMember:
        member_data = self._get_group_admin_member_detail_data(active_user=active_user, group_admin_id=group_admin_id)

        return self._parse_member_data(member_data=member_data, group_admin_id=group_admin_id)

    def group_admin_member_search(
        self,
        active_user: SettingsHelper.get_auth_user_model(),
        term: str,
        group: str = None,
        include_inactive: bool = False,
    ) -> List[ScoutsMember]:
        """
        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#ledenlijst-filterlijst-post
        """
        payload = {"query": term}
        response = requests.get(
            SettingsHelper.get_group_admin_member_search_endpoint(),
            headers={"Authorization": "Bearer {0}".format(active_user.access_token)},
            params=payload,
        )

        response.raise_for_status()
        json = response.json()

        if group:
            return self._parse_search_results_for_group(active_user, json, group, include_inactive=include_inactive)
        else:
            return self._parse_search_results(active_user, json, include_inactive=include_inactive)

    def _parse_search_result(self, member_data) -> ScoutsMember:
        birth_date_str = member_data.get("geboortedatum")
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except:
            birth_date = None

        try:
            # We can only create a basic member with this data
            return ScoutsMember(
                first_name=member_data.get("voornaam"),
                last_name=member_data.get("achternaam"),
                gender=member_data.get("geslacht"),
                email=member_data.get("email"),
                birth_date=birth_date,
                phone_number=member_data.get("gsm"),
                group_admin_id=member_data.get("id"),
            )
        except ValueError:
            # If invalid member just dont add it to results
            pass

        return None

    def _calculate_activity_epoch(self, current_date: date, number_of_years: int) -> date:
        return (current_date - timedelta(days=number_of_years * 365)).date()

    def _parse_search_results(self, active_user, json, include_inactive: bool = False) -> List[ScoutsMember]:
        results = []
        # The "activity epoch" after which a member is deemed a past active member
        activity_epoch = self._calculate_activity_epoch(datetime.now(), 3)

        for member_data in json.get("leden", []):
            member = self._parse_search_result(member_data)
            if member:
                logger.debug(
                    "Requesting detailed member data from GA for member %s",
                    member.group_admin_id,
                )

                detailed_data = self._get_group_admin_member_detail_data(
                    active_user=active_user, group_admin_id=member.group_admin_id
                )

                was_active = False
                end_of_activity_period_counter = 0
                for function in detailed_data.get("functies", []):
                    # Member was active in at least one function since the activity epoch, don't look further
                    if was_active:
                        break

                    end_of_activity_period_str = function.get("einde", None)

                    # Member has ended an activity for at least one function, examine
                    if end_of_activity_period_str:
                        # An end date of a function was registered in the member record
                        end_of_activity_period_counter = end_of_activity_period_counter + 1
                        end_of_activity_period = datetime.fromisoformat(end_of_activity_period_str).date()

                        # Was the end date of the activity after the activity epoch ?
                        if activity_epoch < end_of_activity_period:
                            # Not all insurance types require recently active members to be included in the search results
                            # (currently only temporary insurance for non-members)
                            was_active = True

                            if include_inactive:
                                results.append(self._parse_member_data(detailed_data, member.group_admin_id))

                # The member is still active
                if end_of_activity_period_counter == 0:
                    results.append(self._parse_member_data(detailed_data, member.group_admin_id))

        return results

    def _parse_search_results_for_group(
        self, active_user, json, group: str, include_inactive: bool = False
    ) -> List[ScoutsMember]:
        logger.debug("Filtering members for group %s", group)

        results = []

        for member_data in json.get("leden", []):
            member = self._parse_search_result(member_data)
            if member:
                detailed_data = self._get_group_admin_member_detail_data(
                    active_user=active_user, group_admin_id=member.group_admin_id
                )

                groups = []
                for function in detailed_data.get("functies", []):
                    groups.append(function.get("groep", None))

                if group in groups:
                    results.append(self._parse_member_data(detailed_data, member.group_admin_id))

        return results
