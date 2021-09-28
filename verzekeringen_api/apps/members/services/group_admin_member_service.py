import requests, logging
from datetime import datetime
from django.conf import settings
from apps.locations.utils import PostcodeCity, Address
from ..utils import GroupAdminMember
from ..enums import Sex


logger = logging.getLogger(__name__)


def _get_group_admin_member_detail_data(*, active_user: settings.AUTH_USER_MODEL, group_admin_id:str) -> dict:
    """
        Makes call to IDP to retrieve member details.

    Args:
        active_user (scouts_auth.User): settings.AUTH_USER_MODEL
        group_admin_id (str): foreign id

    Returns: GroupAdminMember

    """
    response = requests.get(
        "{0}/{1}".format(settings.GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT, group_admin_id),
        headers={"Authorization": "Bearer {0}".format(active_user.access_token)},
    )

    response.raise_for_status()
    return response.json()

def _parse_member_data(member_data:dict, group_admin_id:str) -> GroupAdminMember:
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

    address = Address(
        street=raw_address.get("straat"),
        number=raw_address.get("nummer"),
        letter_box=raw_address.get("bus", ""),
        postcode_city=postcode_city,
    )

    member = GroupAdminMember(
        first_name=member_data.get("vgagegevens", {}).get("voornaam"),
        last_name=member_data.get("vgagegevens", {}).get("achternaam"),
        gender=member_data.get("persoonsgegevens", {}).get("geslacht"),
        email=member_data.get("email"),
        birth_date=birth_date,
        phone_number=member_data.get("persoonsgegevens", {}).get("gsm", ""),
        group_admin_id=group_admin_id,
        membership_number=member_data.get("verbondsgegevens", {}).get("lidnummer", ""),
        address=address,
    )

    return member

def group_admin_member_detail(*, active_user: settings.AUTH_USER_MODEL, group_admin_id: str):
    member_data = _get_group_admin_member_detail_data(active_user=active_user, group_admin_id=group_admin_id)

    return _parse_member_data(member_data=member_data, group_admin_id=group_admin_id)


def group_admin_member_search(*, active_user: settings.AUTH_USER_MODEL, term: str, group: str = None) -> list:
    """
    @see https://groepsadmin.scoutsengidsenvlaanderen.be/groepsadmin/client/docs/api.html#ledenlijst-filterlijst-post
    """
    payload = {"query": term}
    response = requests.get(
        settings.GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT,
        headers={"Authorization": "Bearer {0}".format(active_user.access_token)},
        params=payload,
    )

    response.raise_for_status()
    json = response.json()

    if group:
        return _parse_search_results_for_group(active_user, json, group)
    else:
        return _parse_search_results(active_user, json)


def _parse_search_result(member_data) -> GroupAdminMember:
    birth_date_str = member_data.get("geboortedatum")
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except:
        birth_date = None

    try:
        # We can only create a basic member with this data
        return GroupAdminMember(
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


def _parse_search_results(active_user, json):
    results = []

    for member_data in json.get("leden", []):
        member = _parse_search_result(member_data)
        if member:
            results.append(member)

    return results


def _parse_search_results_for_group(active_user, json, group: str):
    logger.debug("Filtering members for group %s", group)

    results = []

    for member_data in json.get("leden", []):
        member = _parse_search_result(member_data)
        if member:
            detailed_data = _get_group_admin_member_detail_data(active_user=active_user, group_admin_id=member.group_admin_id)

            for function in detailed_data.get("functies", []):
                group = function.get("groep", None)

            group_admin_member = group_admin_member_detail(
                active_user=active_user, group_admin_id=member.group_admin_id
            )

            results.append(group_admin_member)

    return results
