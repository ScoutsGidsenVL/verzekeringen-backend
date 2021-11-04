from typing import List
from datetime import datetime

from scouts_auth.models.value_objects import GroupAdminLink


class ScoutsFunction:

    group: str
    function: str
    begin: datetime
    code: str
    description: str
    links: List[GroupAdminLink]

    def __init__(
        self,
        group: str = "",
        function: str = "",
        begin: datetime = None,
        code: str = "",
        description: str = "",
        links: List[GroupAdminLink] = None,
    ):
        self.group = group
        self.function = function
        self.begin = begin
        self.code = code
        self.description = description
        self.links = links if links else []

    def __str__(self):
        return "group({}), function({}), begin({}), code({}), description({}), links({})".format(
            self.group,
            self.function,
            self.begin,
            self.code,
            self.description,
            ", ".join(str(link) for link in self.links),
        )
