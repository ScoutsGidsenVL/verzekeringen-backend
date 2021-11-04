from typing import List

from scouts_auth.models.value_objects import GroupAdminResponse, GroupAdminLink


class GroupAdminMemberListMemberValue:

    key: str
    value: str

    def __init__(self, key: str = "", value: str = ""):
        self.key = key
        self.value = value

    def __str__(self):
        return "[key({}), value({})]".format(self.key, self.value)


class GroupAdminMemberListMember:
    """Partial member data captured in a member list from a call to /ledenlijst."""

    group_admin_id: str
    index: int
    values: List[GroupAdminMemberListMemberValue]
    links: List[GroupAdminLink]

    def __init__(
        self,
        group_admin_id: str = "",
        index: int = 0,
        values: List[GroupAdminMemberListMemberValue] = None,
        links: List[GroupAdminLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.index = index
        self.values = values if values else []
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id({}), index({}), values({}), links({})".format(
            self.group_admin_id,
            self.index,
            ", ".join(str(value) for value in self.values),
            ", ".join(str(link) for link in self.links),
        )


class GroupAdminMemberListResponse(GroupAdminResponse):
    """Class to capture data returned from a call to /ledenlijst."""

    members: List[GroupAdminMemberListMember]

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        criteria: dict = None,
        members: list = None,
        links: List[GroupAdminLink] = None,
    ):
        self.members = members if members else []

        super().__init__(count, total, offset, filter_criterium, criteria, links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(", ".join(str(member) for member in self.members))
