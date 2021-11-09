from typing import List

from groupadmin.models.value_objects import ScoutsGroup, ScoutsLink


class ScoutsGroupListResponse:

    groups: List[ScoutsGroup]
    links: List[ScoutsLink]

    def __init__(self, groups: List[ScoutsGroup] = None, links: List[ScoutsLink] = None):
        self.groups = groups if groups else []
        self.links = links if links else []
