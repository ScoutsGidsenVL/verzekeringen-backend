import requests

from verzekeringen_api import settings
from ..utils import Group, PartialGroup


def get_detailed_group_info(partial_group: PartialGroup) -> Group:
    response = requests.get(partial_group.href)

    response.raise_for_status()
    json = response.json()

    addresses = json.get("adressen", [])
    group = Group(json.get("id"), json.get("naam"), addresses[0].get("gemeente") if addresses else None)

    return group


def get_group_by_number(group_number: str):
    url = '%s/groep/%s' % (settings.GROUP_ADMIN_BASE_URL, group_number)
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return Group(id=data['id'], name=data['naam'], location=None)
