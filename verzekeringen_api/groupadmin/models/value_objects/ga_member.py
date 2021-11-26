from typing import List
from datetime import date

from groupadmin.models.value_objects import (
    ScoutsAddress,
    ScoutsContact,
    ScoutsFunction,
    ScoutsLink,
    ScoutsGroup,
    ScoutsGroupSpecificField,
    ScoutsMemberSearchMember,
)

from inuits.models import Gender, GenderHelper


class ScoutsMemberPersonalData:

    gender: Gender
    phone_number: str

    def __init__(self, gender: Gender = None, phone_number: str = ""):
        self.gender = gender if gender and isinstance(gender, Gender) else GenderHelper.parse_gender(gender)
        self.phone_number = phone_number

    def __str__(self):
        return "gender({}), phone_number({})".format(self.gender, self.phone_number)


class ScoutsMemberGroupAdminData:

    first_name: str
    last_name: str
    birth_date: date

    def __init__(self, first_name: str = "", last_name: str = "", birth_date: date = None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def __str__(self):
        return "first_name({}), last_name({}), birth_date({})".format(self.first_name, self.last_name, self.birth_date)


class ScoutsMemberScoutsData:

    membership_number: str
    customer_number: str

    def __init__(self, membership_number: str = "", customer_number: str = ""):
        self.membership_number = membership_number
        self.customer_number = customer_number

    def __str__(self):
        return "membership_number({}), customer_number({})".format(self.customer_number, self.membership_number)


class ScoutsMember:

    personal_data: ScoutsMemberPersonalData
    group_admin_data: ScoutsMemberGroupAdminData
    scouts_data: ScoutsMemberScoutsData
    email: str
    username: str
    group_admin_id: str
    addresses: List[ScoutsAddress]
    contacts: List[ScoutsContact]
    functions: List[ScoutsFunction]
    scouts_groups: List[ScoutsGroup]
    group_specific_fields: List[ScoutsGroupSpecificField]
    links: List[ScoutsLink]

    def __init__(
        self,
        personal_data: ScoutsMemberPersonalData = None,
        group_admin_data: ScoutsMemberGroupAdminData = None,
        scouts_data: ScoutsMemberScoutsData = None,
        email: str = "",
        username: str = "",
        group_admin_id: str = "",
        addresses: List[ScoutsAddress] = None,
        contacts: List[ScoutsContact] = None,
        functions: List[ScoutsFunction] = None,
        scouts_groups: List[ScoutsGroup] = None,
        group_specific_fields: List[ScoutsGroupSpecificField] = None,
        links: List[ScoutsLink] = None,
    ):
        self.personal_data = personal_data
        self.group_admin_data = group_admin_data
        self.scouts_data = scouts_data
        self.email = email
        self.username = username
        self.group_admin_id = group_admin_id
        self.addresses = addresses if addresses else []
        self.contacts = contacts if contacts else []
        self.functions = functions if functions else []
        self.scouts_groups = scouts_groups if scouts_groups else []
        self.group_specific_fields = group_specific_fields if group_specific_fields else []
        self.links = links if links else []

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    @property
    def gender(self):
        return self.personal_data.gender

    @property
    def phone_number(self):
        return self.personal_data.phone_number

    @property
    def first_name(self):
        return self.group_admin_data.first_name

    @property
    def last_name(self):
        return self.group_admin_data.last_name

    @property
    def birth_date(self):
        return self.group_admin_data.birth_date

    @property
    def membership_number(self):
        return self.scouts_data.membership_number

    @property
    def customer_number(self):
        return self.scouts_data.customer_number

    def __str__(self):
        return (
            self.personal_data.__str__()
            + ", "
            + self.group_admin_data.__str__()
            + ", "
            + self.scouts_data.__str__()
            + ", email({}), username({}), group_admin_id({}), addresses({}), contacts({}), functions({}), groups({}), group_specific_fields ({}), links({})"
        ).format(
            self.email,
            self.username,
            self.group_admin_id,
            ", ".join(str(address) for address in self.addresses),
            ", ".join(str(contact) for contact in self.contacts),
            ", ".join(str(function) for function in self.functions),
            ", ".join(str(group) for group in self.scouts_groups),
            ", ".join(str(field) for field in self.group_specific_fields),
            ", ".join(str(link) for link in self.links),
        )

    def to_search_member(self) -> ScoutsMemberSearchMember:
        member = ScoutsMemberSearchMember(
            group_admin_id=self.group_admin_id,
            first_name=self.group_admin_data.first_name,
            last_name=self.group_admin_data.last_name,
            birth_date=self.group_admin_data.birth_date,
            email=self.email,
            phone_number=self.personal_data.phone_number,
            links=self.links,
        )

        member.gender = self.get_gender()

        return member
