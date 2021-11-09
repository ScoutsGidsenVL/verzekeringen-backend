from typing import List
from datetime import date, datetime

from groupadmin.models.value_objects import ScoutsGroup, ScoutsGrouping, ScoutsLink


class ScoutsFunction:

    group_admin_id: str
    type: str
    group: ScoutsGroup
    function: str
    groups: List[ScoutsGroup]
    groupings: List[ScoutsGrouping]
    begin: datetime
    end: datetime
    max_birth_date: date
    code: str
    description: str
    links: List[ScoutsLink]

    def __init__(
        self,
        group_admin_id: str = "",
        type: str = "",
        group: ScoutsGroup = "",
        function: str = "",
        groups: List[ScoutsGroup] = None,
        groupings: List[ScoutsGrouping] = None,
        begin: datetime = None,
        end: datetime = None,
        max_birth_date: date = None,
        code: str = "",
        description: str = "",
        links: List[ScoutsLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.type = type
        self.group = group
        self.function = function
        self.groups = groups
        self.groupings = groupings
        self.begin = begin
        self.end = end
        self.max_birth_date = max_birth_date
        self.code = code
        self.description = description
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id ({}), type ({}), group({}), function({}), groups({}), groupings({}), begin({}), end ({}), max_birth_date ({}), code({}), description({}), links({})".format(
            self.group_admin_id,
            self.type,
            str(self.group),
            self.function,
            ", ".join(str(group) for group in self.groups),
            ", ".join(str(grouping) for grouping in self.groupings),
            self.begin,
            self.end,
            self.max_birth_date,
            self.code,
            self.description,
            ", ".join(str(link) for link in self.links),
        )
