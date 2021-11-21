from typing import List

from groupadmin.models.value_objects import ScoutsLink


class ScoutsContact:

    member: str
    function: str
    name: str
    phone_number: str
    email: str
    links: List[ScoutsLink]

    def __init__(
        self,
        member: str = "",
        function: str = "",
        name: str = "",
        phone_number: str = "",
        email: str = "",
        links: List[ScoutsLink] = None,
    ):
        self.member = member
        self.function = function
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.links = links if links else []

    def __str__(self):
        return "member({}), function({}), name({}), phone_number({}), email({}), links({})".format(
            self.member,
            self.function,
            self.name,
            self.phone_number,
            self.email,
            ", ".join(str(link) for link in self.links),
        )