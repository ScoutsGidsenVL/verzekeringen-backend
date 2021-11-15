from typing import List

from groupadmin.models.value_objects import ScoutsGroup, ScoutsLink


class ScoutsGroupListResponse:

    groups: List[ScoutsGroup]
    links: List[ScoutsLink]

    def __init__(self, groups: List[ScoutsGroup] = None, links: List[ScoutsLink] = None):
        self.groups = groups.sort(key=lambda group: group.group_admin_id) if groups else []
        self.links = links if links else []
