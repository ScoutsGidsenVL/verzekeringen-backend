from typing import List
from datetime import date, datetime

from groupadmin.models.value_objects import ScoutsGroup, ScoutsGrouping, ScoutsLink
from groupadmin.models.enums import ScoutsFunctionCode
from groupadmin.utils import SettingsHelper


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
    adjunct: str
    links: List[ScoutsLink]

    _scouts_function_code: ScoutsFunctionCode = None

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
        adjunct: str = "",
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
        self.adjunct = adjunct
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id ({}), type ({}), group({}), function({}), groups({}), groupings({}), begin({}), end ({}), max_birth_date ({}), code({}), description({}), adjunct ({}), links({})".format(
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
            self.adjunct,
            ", ".join(str(link) for link in self.links),
        )

    def _parse_function_code(self):
        if self._scouts_function_code is None:
            self._scouts_function_code = ScoutsFunctionCode(self.code)
        return self._scouts_function_code

    def is_district_commissioner(self) -> bool:
        return self._parse_function_code().is_district_commissioner()

    def is_group_leader(self, group: ScoutsGroup) -> bool:
        return self._parse_function_code().is_group_leader() and self.group.group_admin_id == group.group_admin_id

    def is_leader(self, group: ScoutsGroup) -> bool:
        return self._parse_function_code().is_leader() and self.group.group_admin_id == group.group_admin_id
