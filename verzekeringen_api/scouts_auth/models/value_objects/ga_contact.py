from typing import List

from scouts_auth.models.value_objects import GroupAdminLink


class GroupAdminContact:
    
    member: str
    function: str
    name: str
    phone: str
    email: str
    links: List[GroupAdminLink]