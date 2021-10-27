from typing import List

from scouts_auth.models.value_objects import GroupAdminLink


class MemberList:
    """Class to capture data returned from a call to /ledenlijst."""

    count: int = None
    total: int = None
    offset: int = None
    members: list = None
    links: List[GroupAdminLink] = None

    def __init__(
        self,
        count: int = None,
        total: int = None,
        offset: int = None,
        members: list = None,
        links: List[GroupAdminLink] = None,
    ):
        self.count = count if count else 0
        self.total = total if total else 0
        self.offset = offset if offset else 0
        self.members = members if members else []
        self.links = links if links else []


class MemberListMember:

    id: int = None
    values: dict = None
    links: List[GroupAdminLink] = None

    def __init__(self, id: int = None, values: dict = None, links: List[GroupAdminLink] = None):
        self.id = id
        self.values = dict if dict else {}
        self.links = links if links else []
