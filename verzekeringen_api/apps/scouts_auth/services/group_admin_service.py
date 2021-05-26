import requests
from ..utils import Group


def get_detailed_group_info(href: str) -> Group:
    response = requests.get(href)

    response.raise_for_status()
    json = response.json()

    addresses = json.get("adressen", [])
    group = Group(json.get("id"), json.get("naam"), addresses[0].get("gemeente") if addresses else None)

    return group
