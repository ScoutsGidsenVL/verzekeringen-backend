import logging, requests
from typing import List

from scouts_auth.util import SettingsHelper
from scouts_auth.models import (
    User,
    ScoutsGroup,
    GroupAdminMember,
    ScoutsFunction,
    PartialScoutsUser,
    MemberList,
    MemberListMember,
)
from scouts_auth.serializers import GroupAdminMemberSerializer, MemberListSerializer, ScoutsFunctionSerializer


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
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken?query={query}
    url_member_search = SettingsHelper.get_group_admin_member_search_endpoint() + "?query={0}"
    url_member_search_similar = (
        SettingsHelper.get_group_admin_member_search_endpoint() + "/gelijkaardig?voornaam={0}&achternaam={1}"
    )

    def post(self, endpoint: str, payload: dict) -> str:
        """Post the payload to the specified GA endpoint and returns the response as json_data."""
        response = requests.post(endpoint, data=payload)
        response.raise_for_status()

        return response.json()

    def get(self, endpoint: str, active_user: User):
        """Makes a request to the GA with the given url and returns the response as json_data."""
        response = requests.get(endpoint, headers={"Authorization": "Bearer {0}".format(active_user.access_token)})
        response.raise_for_status()

        return response.json()

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    def get_member_info_raw(self, active_user: User, group_admin_id: str) -> str:
        """
        Fetches member info for a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid-get
        """
        json_data = self.get(self.url_member_info.format(group_admin_id), active_user)

        logger.debug("GA CALL: %s (%s)", "get_member_info", self.url_member_info)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_info(self, active_user: User, group_admin_id: str) -> GroupAdminMember:
        json_data = self.get_member_info_raw(active_user, group_admin_id)

        serializer = GroupAdminMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        logger.debug("VALIDATED_DATA: %s (%d)", serializer.validated_data, len(serializer.validated_data.keys()))

        member: GroupAdminMember = serializer.save()

        logger.debug("MEMBER: %s", member)

        return member

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}/steekkaart
    def get_member_medical_flash_card(self, active_user: User, group_admin_id: str) -> str:
        """
        Fetches the medical flash card of a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-individuele-steekkaart-get
        """
        raise NotImplementedError("Fetching the medical flash card of a member has not been implemented yet")

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    def get_groups(self, active_user: User) -> str:
        """
        Fetches a list of all groups for which the authenticated user has rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        json_data = self.get(self.url_groups, active_user)

        logger.debug("GA CALL: %s (%s)", "get_groups", self.url_groups)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/vga
    def get_accountable_groups(self, active_user: User) -> str:
        """
        Fetches a list of all groups for which the authenticated user is a leader (VGA).

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get-1
        """
        json_data = self.get(self.url_groups_vga, active_user)

        logger.debug("GA CALL: %s (%s)", "get_accountable_groups", self.url_groups_vga)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/{group_number}
    def get_group(self, active_user: User, group_number: str) -> str:
        """
        Fetches info of a specific group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groep-get
        """
        json_data = self.get(self.url_group.format(group_number), active_user)

        logger.debug("GA CALL: %s (%s)", "get_group", self.url_group)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep{group_number_fragment_start}
    def get_functions_raw(self, active_user: User, group_number_fragment: str) -> str:
        """
        Fetches a list of functions of the authenticated user for each group.

        The group number can be a complete number, or the first few characters of the group name.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functielijst-get
        """
        json_data = self.get(self.url_functions.format(group_number_fragment), active_user)

        logger.debug("GA CALL: %s (%s)", "get_functions", self.url_functions)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_functions(self, active_user: User, group_number_fragment: str) -> List[ScoutsFunction]:
        json_data = self.get_functions_raw(active_user, group_number_fragment)

        serializer = ScoutsFunctionSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        logger.debug("VALIDATED_DATA: %s (%d)", serializer.validated_data, len(serializer.validated_data.keys()))

        functions: List[ScoutsFunction] = serializer.save()

        logger.debug("FUNCTIONS: %s", functions)

        return functions

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie/{function_id}
    def get_function(self, active_user: User, function_id: str) -> str:
        """
        Fetches info of a specific function.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functie-get
        """
        json_data = self.get(self.url_function.format(function_id), active_user)

        logger.debug("GA CALL: %s (%s)", "get_function", self.url_function)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    def get_member_list_raw(self, active_user: User, offset: int = 0) -> str:
        """
        Fetches a list of members.

        The number returned is based on server load and current response-time. To fetch
        the remainder of the list, the optional offset parameter can be used.

        The type of list returned is determined by an Accept request header:
        - Accept: */* or Accept: application/json_data returns a json_data list
        - Accept: text/csv returns a csv file
        - Accept: application/pdf returns a pdf file

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#ledenlijst-ledenlijst-get
        """
        json_data = self.get(self.url_member_list, active_user)

        logger.debug("GA CALL: %s (%s)", "get_member_list", self.url_member_list)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_list(self, active_user: User, offset: int = 0) -> MemberList:
        json_data = self.get_member_list_raw(active_user, offset)

        serializer = MemberListSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        logger.debug("VALIDATED_DATA: %s (%d)", serializer.validated_data, len(serializer.validated_data.keys()))

        member_list: MemberList = serializer.save()

        logger.debug("MEMBER LIST: %s", member_list)

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/query={query}
    def search_member(self, active_user: User, query: str) -> str:
        """
        Fetches a list of members that have info similar to the search term.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-zoeken-get
        """
        json_data = self.get(self.url_member_search.format(query), active_user)
        logger.info("%s", json_data)
        logger.debug("GA CALL: %s (%s)", "search_member", self.url_member_search)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/gelijkaardig?voornaam={first_name}&achternaam={last_name}
    def search_similar_member(self, active_user: User, first_name: str, last_name: str) -> str:
        """
        Fetches a list of members that have a name similar to the first_name and last_name arguments.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-gelijkaardig-zoeken-get
        """
        json_data = self.get(self.url_member_search_similar.format(first_name, last_name), active_user)

        logger.debug("GA CALL: %s (%s)", "search_similar_member", self.url_member_search_similar)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data
