from typing import List

from groupadmin.models.value_objects import ScoutsLink


class ScoutsAllowedCalls:
    links: List[ScoutsLink]

    def __init__(self, links: List[ScoutsLink] = None):
        self.links = links if links else []

    def __str__(self):
        return "links({})".format(", ".join(link for link in self.links))
