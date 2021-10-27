import logging, requests

from django.conf import settings

from scouts_auth.models import ScoutsGroup, PartialScoutsGroup
from scouts_auth.util import SettingsHelper

logger = logging.getLogger(__name__)


class GroupAdminGroupService:
    def get_detailed_group(self, partial_group: PartialScoutsGroup) -> ScoutsGroup:
        logger.debug(
            "SCOUTS_AUTH: getting detailed group info for %s from %s",
            partial_group.id,
            partial_group.href,
        )
        response = requests.get(partial_group.href)

        response.raise_for_status()
        json = response.json()

        addresses = json.get("adressen", [])

        logger.debug("SCOUTS_AUTH: addressen")
        logger.debug(addresses)

        return ScoutsGroup(
            json.get("id"),
            json.get("naam"),
            partial_group.href,
            addresses[0].get("gemeente") if addresses else None,
        )

    def get_group_by_number(self, group_number: str) -> ScoutsGroup:
        url = "%s/groep/%s" % (SettingsHelper.get_group_admin_base_url(), group_number)
        response = requests.get(url)
        if response.ok:
            data = response.json()
            return ScoutsGroup(identifier=data["id"], name=data["naam"], location=None)
