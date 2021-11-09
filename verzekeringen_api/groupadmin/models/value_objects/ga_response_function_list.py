from typing import List

from groupadmin.models.value_objects import ScoutsFunction, ScoutsLink


class ScoutsFunctionListResponse:

    functions: List[ScoutsFunction]
    links: List[ScoutsLink]

    def __init__(self, functions: List[ScoutsFunction] = None, links: List[ScoutsLink] = None):
        self.functions = functions if functions else []
        self.links = links if links else []

    def __str__(self):
        return "functions({}), links({})".format(
            ", ".join(str(function) for function in self.functions), ", ".join(str(link) for link in self.links)
        )
