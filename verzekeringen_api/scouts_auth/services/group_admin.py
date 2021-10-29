import logging, requests
from typing import List

from scouts_auth.util import SettingsHelper
from scouts_auth.models import User, ScoutsGroup, GroupAdminMember, ScoutsFunction, PartialScoutsUser, MemberListMember


logger = logging.getLogger(__name__)


class GroupAdmin:

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    url_member_info = SettingsHelper.get_group_admin_member_detail_endpoint() + "/{0}"
    url_member_medical_flash_card = SettingsHelper.get_group_admin_member_detail_endpoint() + "/steekkaart"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    url_groups = SettingsHelper.get_group_admin_group_endpoint()
    url_groups_vga = SettingsHelper.get_group_admin_group_endpoint() + "/vga"
    url_group = SettingsHelper.get_group_admin_group_endpoint() + "/{0}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep={group_number_start_fragment}
    url_functions = SettingsHelper.get_group_admin_functions_endpoint() + "?groep={0}"
    url_function = SettingsHelper.get_group_admin_functions_endpoint() + "/{0}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    url_member_list = SettingsHelper.get_group_admin_member_list_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/query={query}
    url_member_search = SettingsHelper.get_group_admin_member_search_endpoint() + "/query={0}"
    url_member_search_similar = (
        SettingsHelper.get_group_admin_member_search_endpoint() + "/gelijkaardig?voornaam={0}&achternaam={1}"
    )

    def auth_request(self, endpoint: str, payload: dict) -> str:
        response = requests.post(endpoint, data=payload)

        response.raise_for_status()

        return response.json()

    def request(self, active_user: User, href: str):
        """Makes a request to the GA with the given url and returns the response as json."""
        response = requests.get(href, headers={"Authorization": "Bearer {0}".format(active_user.access_token)})
        response.raise_for_status()

        return response.json()

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    def get_member_info(self, active_user: User, group_admin_id: str) -> GroupAdminMember:
        """
        Fetches member info for a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid-get
        """
        json = self.request(active_user, self.url_member_info.format(group_admin_id))

        logger.debug("GA CALL: %s", "get_member_info")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}/steekkaart
    def get_member_medical_flash_card(self, active_user: User, group_admin_id: str):
        """
        Fetches the medical flash card of a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-individuele-steekkaart-get
        """
        raise NotImplementedError("Fetching the medical flash card of a member has not been implemented yet")

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    def get_groups(self, active_user: User) -> List[ScoutsGroup]:
        """
        Fetches a list of all groups for which the authenticated user has rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        json = self.request(active_user, self.url_groups)

        logger.debug("GA CALL: %s", "get_groups")
        logger.debug("GA RESPONSE: %s", json)

        return json.get("groepen")

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/vga
    def get_accountable_groups(self, active_user: User):
        """
        Fetches a list of all groups for which the authenticated user is a leader (VGA).

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get-1
        """
        json = self.request(active_user, self.url_groups_vga)

        logger.debug("GA CALL: %s", "get_accountable_groups")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/{group_number}
    def get_group(self, active_user: User, group_number: str) -> ScoutsGroup:
        """
        Fetches info of a specific group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groep-get
        """
        json = self.request(active_user, self.url_group.format(group_number))

        logger.debug("GA CALL: %s", "get_group")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep{group_number_fragment_start}
    def get_functions(self, active_user: User, group_number_fragment: str) -> List[ScoutsFunction]:
        """
        Fetches a list of functions of the authenticated user for each group.

        The group number can be a complete number, or the first few characters of the group name.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functielijst-get
        """
        json = self.request(active_user, self.url_functions.format(group_number_fragment))

        logger.debug("GA CALL: %s", "get_functions")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie/{function_id}
    def get_function(self, active_user: User, function_id: str) -> ScoutsFunction:
        """
        Fetches info of a specific function.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functie-get
        """
        json = self.request(active_user, self.url_function.format(function_id))

        logger.debug("GA CALL: %s", "get_function")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    def get_member_list(self, active_user: User, offset: int = None) -> List[MemberListMember]:
        """
        Fetches a list of members.

        The number returned is based on server load and current response-time. To fetch
        the remainder of the list, the optional offset parameter can be used.

        The type of list returned is determined by an Accept request header:
        - Accept: */* or Accept: application/json returns a json list
        - Accept: text/csv returns a csv file
        - Accept: application/pdf returns a pdf file

        A

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#ledenlijst-ledenlijst-get
        """
        json = self.request(active_user, self.url_member_list)

        logger.debug("GA CALL: %s", "get_member_list")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/query={query}
    def search_member(self, active_user: User, query: str) -> List[PartialScoutsUser]:
        """
        Fetches a list of members that have info similar to the search term.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-zoeken-get
        """
        json = self.request(active_user, self.url_member_search.format(query))
        logger.info("%s", json)
        logger.debug("GA CALL: %s", "search_member")
        logger.debug("GA RESPONSE: %s", json)

        return json

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/gelijkaardig?voornaam={first_name}&achternaam={last_name}
    def search_similar_member(self, active_user: User, first_name: str, last_name: str) -> List[PartialScoutsUser]:
        """
        Fetches a list of members that have a name similar to the first_name and last_name arguments.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-gelijkaardig-zoeken-get
        """
        json = self.request(active_user, self.url_member_search_similar.format(first_name, last_name))

        logger.debug("GA CALL: %s", "search_similar_member")
        logger.debug("GA RESPONSE: %s", json)

        return json
