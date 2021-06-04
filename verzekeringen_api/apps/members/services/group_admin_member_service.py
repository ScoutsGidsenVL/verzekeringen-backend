import requests
from datetime import datetime
from django.conf import settings
from apps.locations.utils import PostcodeCity, Address
from ..utils import GroupAdminMember


def group_admin_member_detail(*, active_user: settings.AUTH_USER_MODEL, group_admin_id: str):
    response = requests.get(
        "{0}/{1}".format(settings.GROUP_ADMIN_MEMBER_DETAIL_ENDPOINT, group_admin_id),
        headers={"Authorization": "Bearer {0}".format(active_user.access_token)},
    )

    response.raise_for_status()
    member_data = response.json()

    birth_date_str = member_data.get("geboortedatum")
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
    except:
        birth_date = None

    addresses = member_data.get("adressen", [])
    if len(addresses) == 0:
        raise Error("Something went wrong, chosen member has no address")
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
        email=member_data.get("email"),
        birth_date=birth_date,
        phone_number=member_data.get("persoonsgegevens", {}).get("gsm", ""),
        group_admin_id=group_admin_id,
        membership_number=member_data.get("verbondsgegevens", {}).get("lidnummer", ""),
        address=address,
    )

    return member


def group_admin_member_search(*, active_user: settings.AUTH_USER_MODEL, term: str) -> list:
    payload = {"query": term}
    response = requests.get(
        settings.GROUP_ADMIN_MEMBER_SEARCH_ENDPOINT,
        headers={"Authorization": "Bearer {0}".format(active_user.access_token)},
        params=payload,
    )

    response.raise_for_status()
    json = response.json()

    results = []
    for member_data in json.get("leden", []):
        birth_date_str = member_data.get("geboortedatum")
        try:
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d").date()
        except:
            birth_date = None
        try:
            # We can only create a basic member with this data
            results.append(
                GroupAdminMember(
                    first_name=member_data.get("voornaam"),
                    last_name=member_data.get("achternaam"),
                    email=member_data.get("email"),
                    birth_date=birth_date,
                    phone_number=member_data.get("gsm"),
                    group_admin_id=member_data.get("id"),
                )
            )
        except ValueError:
            # If invalid member just dont add it to results
            pass

    return results
