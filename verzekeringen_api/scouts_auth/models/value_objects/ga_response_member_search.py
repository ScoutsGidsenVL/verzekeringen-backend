from typing import List
from datetime import date

from scouts_auth.models.value_objects import GroupAdminResponse, GroupAdminLink


class GroupAdminMemberSearchMember:

    group_admin_id: str
    first_name: str
    last_name: str
    birth_date: date
    email: str
    phone: str
    links: List[GroupAdminLink]

    def __init__(
        self,
        group_admin_id: str = "",
        first_name: str = "",
        last_name: str = "",
        birth_date: date = None,
        email: str = "",
        phone: str = "",
        links: List[GroupAdminLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.phone = phone
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id({}), first_name({}), last_name({}), birth_date({}), email({}), phone({}), links({})".format(
            self.group_admin_id,
            self.first_name,
            self.last_name,
            self.birth_date,
            self.email,
            self.phone,
            ", ".join(str(link) for link in self.links),
        )


class GroupAdminMemberSearchResponse(GroupAdminResponse):
    """Class to capture data returned from a call to /ledenlijst."""

    members: List[GroupAdminMemberSearchMember]

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        criteria: dict = None,
        members: List[GroupAdminMemberSearchMember] = None,
        links: List[GroupAdminLink] = None,
    ):
        self.members = members if members else []

        super().__init__(count, total, offset, filter_criterium, criteria, links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(", ".join(str(member) for member in self.members))
