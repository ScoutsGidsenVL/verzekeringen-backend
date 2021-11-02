from typing import List

from django.db import models

from scouts_auth.models.value_objects import GroupAdminLink

from inuits.models import AbstractModel
from inuits.models.fields import OptionalCharField, OptionalIntegerField


class MemberListMember(AbstractModel):
    """Partial member data captured in a member list from a call to /ledenlijst."""

    group_admin_id: str = OptionalCharField()
    index: int = OptionalIntegerField()
    values: dict = None
    links: List[GroupAdminLink]

    def __init__(
        self, group_admin_id: str = "", index: int = 0, values: dict = None, links: List[GroupAdminLink] = None
    ):
        self.group_admin_id = group_admin_id
        self.index = index
        self.values = values if values else {}
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id(%s), index(%d), values(%s), links(%s)".format(
            self.group_admin_id,
            self.index,
            self.values,
            ", ".join(str(link) for link in self.links),
        )


class MemberList(AbstractModel):
    """Class to capture data returned from a call to /ledenlijst."""

    count: int = OptionalIntegerField()
    total: int = OptionalIntegerField()
    offset: int = OptionalIntegerField()
    filter_criterium: str = OptionalCharField()
    members: List[MemberListMember]
    links: List[GroupAdminLink]

    def __init__(
        self,
        count: int = 0,
        total: int = 0,
        offset: int = 0,
        filter_criterium: str = "",
        members: list = None,
        links: List[GroupAdminLink] = None,
    ):
        self.count = count
        self.total = total
        self.offset = offset
        self.filter_criterium = filter_criterium
        self.members = members if members else []
        self.links = links if links else []

    def __str__(self):
        return "count({}), total({}), offset({}), filter_criterium({}), members: ({}), links: ({})".format(
            self.count,
            self.total,
            self.offset,
            self.filter_criterium,
            ", ".join(str(member) for member in self.members),
            ", ".join(str(link) for link in self.links),
        )
