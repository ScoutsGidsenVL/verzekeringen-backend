import logging, requests

from django.http import Http404
from rest_framework import status
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.models import User

from groupadmin.models import (
    ScoutsAllowedCalls,
    ScoutsFunction,
    ScoutsFunctionListResponse,
    ScoutsGroup,
    ScoutsGroupListResponse,
    ScoutsMemberSearchResponse,
    ScoutsMember,
    ScoutsMemberListResponse,
)
from groupadmin.serializers import (
    ScoutsAllowedCallsSerializer,
    ScoutsFunctionSerializer,
    ScoutsFunctionListResponseSerializer,
    ScoutsGroupSerializer,
    ScoutsGroupListResponseSerializer,
    ScoutsMemberSearchResponseSerializer,
    ScoutsMemberListResponseSerializer,
    ScoutsMemberSerializer,
)

from groupadmin.utils import SettingsHelper


logger = logging.getLogger(__name__)


class GroupAdmin:

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/
    url_allowed_calls = SettingsHelper.get_group_admin_allowed_calls_endpoint() + "/"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    url_groups = SettingsHelper.get_group_admin_group_endpoint()
    url_groups_vga = SettingsHelper.get_group_admin_group_endpoint() + "/vga"
    url_group = SettingsHelper.get_group_admin_group_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep={group_number_start_fragment}
    url_functions = SettingsHelper.get_group_admin_functions_endpoint() + "?groep={}"
    url_function = SettingsHelper.get_group_admin_functions_endpoint() + "/{}"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    url_member_profile = SettingsHelper.get_group_admin_profile_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/ledenlijst
    url_member_list = SettingsHelper.get_group_admin_member_list_endpoint()
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    url_member_info = SettingsHelper.get_group_admin_member_detail_endpoint() + "/{}"
    url_member_medical_flash_card = SettingsHelper.get_group_admin_member_detail_endpoint() + "/steekkaart"
    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken?query={query}
    url_member_search = SettingsHelper.get_group_admin_member_search_endpoint() + "?query={}"
    url_member_search_similar = (
        SettingsHelper.get_group_admin_member_search_endpoint() + "/gelijkaardig?voornaam={}&achternaam={}"
    )

    def post(self, endpoint: str, payload: dict) -> str:
        """Post the payload to the specified GA endpoint and returns the response as json_data."""
        logger.debug("GA: Posting data to endpoint %s", endpoint)
        try:
            response = requests.post(endpoint, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error

        return response.json()

    def get(self, endpoint: str, active_user: User):
        """Makes a request to the GA with the given url and returns the response as json_data."""
        logger.debug("GA: Fetching data from endpoint %s", endpoint)
        try:
            response = requests.get(endpoint, headers={"Authorization": "Bearer {0}".format(active_user.access_token)})
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error

        return response.json()

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/
    def get_allowed_calls_raw(self, active_user: User) -> str:
        """
        Fetches a list of all groupadmin calls that the authenticated user can make

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#overzicht-overzicht-get
        """
        json_data = self.get(self.url_allowed_calls, active_user)

        logger.info("GA CALL: %s (%s)", "get_allowed_calls", self.url_allowed_calls)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsAllowedCallsSerializer},
    )
    def get_allowed_calls(self, active_user: User) -> ScoutsAllowedCalls:
        json_data = self.get_allowed_calls_raw(active_user)

        serializer = ScoutsAllowedCallsSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        allowed_calls: ScoutsAllowedCalls = serializer.save()

        return allowed_calls

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep
    def get_groups_raw(self, active_user: User) -> str:
        """
        Fetches a list of all groups for which the authenticated user has rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get
        """
        json_data = self.get(self.url_groups, active_user)

        logger.info("GA CALL: %s (%s)", "get_groups", self.url_groups)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_groups(self, active_user: User) -> ScoutsGroupListResponse:
        json_data = self.get_groups_raw(active_user)

        serializer = ScoutsGroupListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: ScoutsGroupListResponse = serializer.save()

        return groups_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/vga
    def get_accountable_groups_raw(self, active_user: User) -> str:
        """
        Fetches a list of all groups for which the authenticated user is a leader (VGA).

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groepen-get-1
        """
        json_data = self.get(self.url_groups_vga, active_user)

        logger.info("GA CALL: %s (%s)", "get_accountable_groups", self.url_groups_vga)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_accountable_groups(self, active_user: User) -> ScoutsGroupListResponse:
        json_data = self.get_accountable_groups_raw(active_user)

        serializer = ScoutsGroupListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        groups_response: ScoutsGroupListResponse = serializer.save()

        return groups_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/groep/{group_number}
    def get_group_raw(self, active_user: User, group_number: str) -> str:
        """
        Fetches info of a specific group.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#groepen-groep-get
        """
        json_data = self.get(self.url_group.format(group_number), active_user)

        logger.info("GA CALL: %s (%s)", "get_group", self.url_group)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_group(self, active_user: User, group_number: str) -> ScoutsGroup:
        json_data = self.get_group_raw(active_user, group_number)

        serializer = ScoutsGroupSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        group: ScoutsGroup = serializer.save()

        return group

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie?groep{group_number_fragment_start}
    def get_functions_raw(self, active_user: User, group_number_fragment: str) -> str:
        """
        Fetches a list of functions of the authenticated user for each group.

        The group number can be a complete number, or the first few characters of the group name.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functielijst-get
        """
        json_data = self.get(self.url_functions.format(group_number_fragment), active_user)

        logger.info("GA CALL: %s (%s)", "get_functions", self.url_functions)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_functions(self, active_user: User, group_number_fragment: str) -> ScoutsFunctionListResponse:
        json_data = self.get_functions_raw(active_user, group_number_fragment)

        serializer = ScoutsFunctionListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        function_response: ScoutsFunctionListResponse = serializer.save()

        return function_response

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/functie/{function_id}
    def get_function_raw(self, active_user: User, function_id: str) -> str:
        """
        Fetches info of a specific function.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#functies-functie-get
        """
        json_data = self.get(self.url_function.format(function_id), active_user)

        logger.info("GA CALL: %s (%s)", "get_function", self.url_function)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_function(self, active_user: User, function_id: str) -> ScoutsFunction:
        json_data = self.get_function_raw(active_user, function_id)

        serializer = ScoutsFunctionSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        function: ScoutsFunction = serializer.save()

        return function

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/profiel
    def get_member_profile_raw(self, active_user: User) -> str:
        """
        Fetches the profile information of the current user.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid
        """
        json_data = self.get(self.url_member_profile, active_user)

        logger.info("GA CALL: %s (%s)", "get_member_profile", self.url_function)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_profile(self, active_user: User) -> ScoutsMember:
        json_data = self.get_member_profile_raw(active_user)

        serializer = ScoutsMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: ScoutsMember = serializer.save()

        return member

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}
    def get_member_info_raw(self, active_user: User, group_admin_id: str) -> str:
        """
        Fetches member info for a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-lid-get
        """
        json_data = self.get(self.url_member_info.format(group_admin_id), active_user)

        logger.info("GA CALL: %s (%s)", "get_member_info", self.url_member_info)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_info(self, active_user: User, group_admin_id: str) -> ScoutsMember:
        json_data = self.get_member_info_raw(active_user, group_admin_id)

        serializer = ScoutsMemberSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member: ScoutsMember = serializer.save()

        return member

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/lid/{group_admin_id}/steekkaart
    def get_member_medical_flash_card(self, active_user: User, group_admin_id: str) -> str:
        """
        Fetches the medical flash card of a member for which the authenticated user has read rights.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#leden-individuele-steekkaart-get
        """
        raise NotImplementedError("Fetching the medical flash card of a member has not been implemented yet")

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

        logger.info("GA CALL: %s (%s)", "get_member_list", self.url_member_list)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def get_member_list(self, active_user: User, offset: int = 0) -> ScoutsMemberListResponse:
        json_data = self.get_member_list_raw(active_user, offset)

        serializer = ScoutsMemberListResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: ScoutsMemberListResponse = serializer.save()

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/query={query}
    def search_member_raw(self, active_user: User, term: str) -> str:
        """
        Fetches a list of members that have info similar to the search term.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-zoeken-get
        """
        json_data = self.get(self.url_member_search.format(term), active_user)

        logger.info("GA CALL: %s (%s)", "search_member", self.url_member_search)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data

    def search_member(self, active_user: User, term: str, group: str = None) -> ScoutsMemberSearchResponse:
        json_data = self.search_member_raw(active_user, term)

        serializer = ScoutsMemberSearchResponseSerializer(data=json_data)
        serializer.is_valid(raise_exception=True)

        member_list: ScoutsMemberSearchResponse = serializer.save()

        return member_list

    # https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/rest-ga/zoeken/gelijkaardig?voornaam={first_name}&achternaam={last_name}
    def search_similar_member(self, active_user: User, first_name: str, last_name: str) -> str:
        """
        Fetches a list of members that have a name similar to the first_name and last_name arguments.

        @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#zoeken-gelijkaardig-zoeken-get
        """
        json_data = self.get(self.url_member_search_similar.format(first_name, last_name), active_user)

        logger.info("GA CALL: %s (%s)", "search_similar_member", self.url_member_search_similar)
        logger.debug("GA RESPONSE: %s", json_data)

        return json_data
