from typing import List
from datetime import datetime

from django.db import models

from scouts_auth.models.enums import Gender, GenderHelper
from scouts_auth.models.value_objects import GroupAdminAddress, GroupAdminContact, ScoutsFunction, GroupAdminLink

from inuits.models import AbstractModel
from inuits.models.fields import OptionalCharField, OptionalDateField, OptionalIntegerField


class GroupAdminMember(AbstractModel):

    gender: Gender = models.CharField(max_length=1, choices=Gender.choices, default=Gender.UNKNOWN)
    phone_number: str = OptionalCharField()
    first_name: str = OptionalCharField()
    last_name: str = OptionalCharField()
    birth_date: datetime.date = OptionalDateField()
    membership_number: str = OptionalCharField()
    customer_number: str = OptionalCharField()
    email: str = OptionalCharField()
    username: str = OptionalCharField()
    group_admin_id: str = OptionalCharField()
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
