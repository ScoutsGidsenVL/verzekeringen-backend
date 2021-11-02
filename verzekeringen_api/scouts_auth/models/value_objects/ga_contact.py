from typing import List

from scouts_auth.models.value_objects import GroupAdminLink

from inuits.models import AbstractModel
from inuits.models.fields import OptionalCharField


class GroupAdminContact(AbstractModel):

    member: str = OptionalCharField()
    function: str = OptionalCharField()
    name: str = OptionalCharField()
    phone: str = OptionalCharField()
    email: str = OptionalCharField()
    links: List[GroupAdminLink]

    def __init__(
        self,
        member: str = "",
        function: str = "",
        name: str = "",
        phone: str = "",
        email: str = "",
        links: List[GroupAdminLink] = None,
    ):
        self.member = member
        self.function = function
        self.name = name
        self.phone = phone
        self.email = email
        self.links = links if links else []

    def __str__(self):
        return "member({}), function({}), name({}), phone({}), email({}), links({})".format(
            self.member,
            self.function,
            self.name,
            self.phone,
            self.email,
            ", ".join(str(link) for link in self.links),
        )
