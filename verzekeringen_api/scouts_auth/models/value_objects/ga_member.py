from typing import List
from datetime import date, datetime

from scouts_auth.models.enums import Gender, GenderHelper
from scouts_auth.models.value_objects import GroupAdminAddress, GroupAdminContact, ScoutsFunction, GroupAdminLink


class GroupAdminMemberGroupAdminData:
    first_name: str
    last_name: str
    birth_date: date

    def __init__(self, first_name: str = "", last_name: str = "", birth_date: date = None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def __str__(self):
        return "first_name({}), last_name({}), birth_date({})".format(self.first_name, self.last_name, self.birth_date)


class GroupAdminMemberScoutsData:
    membership_number: str
    customer_number: str

    def __init__(self, membership_number: str = "", customer_number: str = ""):
        self.membership_number = membership_number
        self.customer_number = customer_number

    def __str__(self):
        return "membership_number({}), customer_number({})".format(self.customer_number, self.membership_number)


class GroupAdminMember:

    gender: Gender
    phone_number: str
    first_name: str
    last_name: str
    birth_date: datetime.date
    membership_number: str
    customer_number: str
    email: str
    username: str
    group_admin_id: str
    addresses: List[GroupAdminAddress]
    contacts: List[GroupAdminContact]
    functions: List[ScoutsFunction]
    links: List[GroupAdminLink]

    def __init__(
        self,
        gender: Gender = None,
        phone_number: str = "",
        first_name: str = "",
        last_name: str = "",
        birth_date: datetime.date = None,
        membership_number: str = "",
        customer_number: str = "",
        email: str = "",
        username: str = "",
        group_admin_id: str = "",
        addresses: List[GroupAdminAddress] = None,
        contacts: List[GroupAdminContact] = None,
        functions: List[ScoutsFunction] = None,
        links: List[GroupAdminLink] = None,
    ):
        self.gender = gender if gender and isinstance(gender, Gender) else GenderHelper.parse_gender(gender)
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.membership_number = membership_number
        self.customer_number = customer_number
        self.email = email
        self.username = username
        self.group_admin_id = group_admin_id
        self.addresses = addresses if addresses else []
        self.contacts = contacts if contacts else []
        self.functions = functions if functions else []
        self.links = links if links else []

    def get_gender(self):
        return self.gender

    def __str__(self):
        return "gender({}), phone_number({}), first_name({}), last_name({}), birth_date({}), membership_number({}), customer_number({}), email({}), username({}), group_admin_id({}), addresses({}), contacts({}), functions({}), links({})".format(
            self.gender,
            self.phone_number,
            self.first_name,
            self.last_name,
            self.birth_date,
            self.membership_number,
            self.customer_number,
            self.email,
            self.username,
            self.group_admin_id,
            ", ".join(str(address) for address in self.addresses),
            ", ".join(str(contact) for contact in self.contacts),
            ", ".join(str(function) for function in self.functions),
            ", ".join(str(link) for link in self.links),
        )
