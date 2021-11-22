from typing import List

from groupadmin.models.value_objects import ScoutsGroup, ScoutsLink


class ScoutsGroupListResponse:

    scouts_groups: List[ScoutsGroup]
    links: List[ScoutsLink]

    def __init__(self, scouts_groups: List[ScoutsGroup] = None, links: List[ScoutsLink] = None):
        self.scouts_groups = scouts_groups.sort(key=lambda group: group.group_admin_id) if scouts_groups else []
        self.links = links if links else []
