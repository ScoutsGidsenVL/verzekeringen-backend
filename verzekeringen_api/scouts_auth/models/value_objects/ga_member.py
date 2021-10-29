from typing import List
from datetime import datetime

from scouts_auth.models.enums import Gender, GenderHelper
from scouts_auth.models.value_objects import GroupAdminAddress, GroupAdminContact, ScoutsFunction


class GroupAdminMember:
    first_name: str
    last_name: str
    gender: Gender
    phone_number: str
    birth_date: datetime.date
    email: str
    group_admin_id: str
    membership_number: int
    username: str
    addresses: List[GroupAdminAddress]
    contacts: List[GroupAdminContact]
    functions: List[ScoutsFunction]

    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        gender: Gender = None,
        phone_number: str = None,
        birth_date: datetime.date = None,
        email: str = None,
        group_admin_id: str = None,
        membership_number: str = None,
        username: str = None,
        addresses: List[GroupAdminAddress] = None,
        contacts: List[GroupAdminContact] = None,
        functions: List[ScoutsFunction] = None,
    ):
        if not first_name or not last_name or not group_admin_id:
            raise ValueError("first_name, last_name and group_admin_id can not be empty")

        self.first_name = first_name if first_name else ""
        self.last_name = last_name if last_name else ""
        self.gender = GenderHelper.parse_gender(gender)
        self.phone_number = phone_number if phone_number else ""
        self.birth_date = birth_date
        self.email = email if email else ""
        self.group_admin_id = group_admin_id if group_admin_id else ""
        self.membership_number = membership_number if membership_number else ""
        self.username = username if username else ""
        self.addresses = addresses if addresses else []
        self.contacts = contacts if contacts else []
        self.functions = functions if functions else []

    def get_gender(self):
        return self.gender
