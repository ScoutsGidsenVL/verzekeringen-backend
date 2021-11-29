from typing import List, Tuple

from scouts_auth.groupadmin.models.value_objects import ScoutsFunction, ScoutsLink


class ScoutsFunctionListResponse:

    functions: List[ScoutsFunction]
    links: List[ScoutsLink]

    def __init__(self, functions: List[ScoutsFunction] = None, links: List[ScoutsLink] = None):
        self.functions = functions if functions else []
        self.links = links if links else []

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    def get_descriptive_function_codes(self) -> List[Tuple]:
        return [(function.code, function.description) for function in self.functions]

    def get_printable_descriptive_function_codes(self) -> str:
        return "\n".join(function.code + "," + function.description for function in self.functions)

    def __str__(self):
        return "functions({}), links({})".format(
            ", ".join(str(function) for function in self.functions), ", ".join(str(link) for link in self.links)
        )
