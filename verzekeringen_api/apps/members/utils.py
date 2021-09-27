from django.db import models
from datetime import datetime
from apps.locations.utils import Address
from .enums import Sex


class GroupAdminMember:
    first_name: str
    last_name: str
    gender: Sex
    phone_number: str
    birth_date: datetime.date
    email: str
    group_admin_id: str

    membership_number: int
    address: Address

    def __init__(
        self,
        first_name,
        last_name,
        gender,
        phone_number,
        birth_date,
        email,
        group_admin_id,
        membership_number=None,
        address=None,
    ):
        if not first_name or not last_name or not group_admin_id:
            raise ValueError("first_name, last_name and group_admin_id can not be empty")
        if not gender or gender not in (Sex.MALE.label, Sex.FEMALE.label, Sex.OTHER.label):
            gender = Sex.UNKNOWN

        self.first_name = first_name
        self.last_name = last_name
        self.gender = gender
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.email = email
        self.group_admin_id = group_admin_id
        self.membership_number = membership_number
        self.address = address

    def get_sex(self) -> Sex:
        return self.gender
