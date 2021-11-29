from typing import List
from datetime import date

from scouts_auth.groupadmin.models.value_objects import ScoutsResponse, ScoutsLink

from scouts_auth.inuits.models import Gender


class ScoutsMemberSearchMember:

    group_admin_id: str
    first_name: str
    last_name: str
    birth_date: date
    email: str
    phone_number: str
    gender: Gender
    links: List[ScoutsLink]

    def __init__(
        self,
        group_admin_id: str = "",
        first_name: str = "",
        last_name: str = "",
        birth_date: date = None,
        email: str = "",
        phone_number: str = "",
        links: List[ScoutsLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.email = email
        self.phone_number = phone_number
        self.links = links if links else []

    def get_gender(self):
        return self.gender

    def __str__(self):
        return "group_admin_id({}), first_name({}), last_name({}), birth_date({}), email({}), phone_number({}), links({})".format(
            self.group_admin_id,
            self.first_name,
            self.last_name,
            self.birth_date,
            self.email,
            self.phone_number,
            ", ".join(str(link) for link in self.links),
        )


class ScoutsMemberSearchResponse(ScoutsResponse):
    """Class to capture data returned from a call to /ledenlijst."""

    members: List[ScoutsMemberSearchMember]

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        criteria: dict = None,
        members: List[ScoutsMemberSearchMember] = None,
        links: List[ScoutsLink] = None,
    ):
        self.members = members if members else []

        super().__init__(count, total, offset, filter_criterium, criteria, links)

    def __str__(self):
        return ("members: ({}), " + super().__str__()).format(", ".join(str(member) for member in self.members))
