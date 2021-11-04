from typing import List

from scouts_auth.models.value_objects import ScoutsGroup, GroupAdminLink


class ResponseScoutsGroup:

    groups: List[ScoutsGroup]
    links: List[GroupAdminLink]

    def __init__(self, groups: List[ScoutsGroup] = None, links: List[GroupAdminLink] = None):
        self.groups = groups if groups else []
        self.links = links if links else []
