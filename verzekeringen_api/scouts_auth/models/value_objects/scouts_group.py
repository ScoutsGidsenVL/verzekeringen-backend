from typing import List
from datetime import date

from django.db import models

from scouts_auth.models.value_objects import GroupAdminAddress, GroupAdminContact, GroupAdminLink

from inuits.models import AbstractModel
from inuits.models.fields import OptionalCharField, OptionalDateField


class ScoutsGroup(AbstractModel):
    """Models the scouts groups a user has rights to."""

    group_admin_id: str = OptionalCharField()
    number: str = OptionalCharField()
    name: str = OptionalCharField()
    addresses: List[GroupAdminAddress]
    date_of_foundation: date = OptionalDateField
    only_leaders: bool = models.BooleanField
    show_members_improved: bool = models.BooleanField
    bank_account: str = OptionalCharField()
    email: str = OptionalCharField()
    website: str = OptionalCharField()
    info: str = OptionalCharField()
    type: str = OptionalCharField()
    contacts: List[GroupAdminContact]
    links: List[GroupAdminLink]

    def __init__(
        self,
        group_admin_id: str = "",
        number: str = "",
        name: str = "",
        addresses: List[GroupAdminAddress] = None,
        date_of_foundation: date = None,
        only_leaders: bool = False,
        show_members_improved: bool = False,
        bank_account: str = "",
        email: str = "",
        website: str = "",
        info: str = "",
        type: str = "",
        contacts: List[GroupAdminContact] = None,
        links: List[GroupAdminLink] = None,
    ):
        self.group_admin_id = group_admin_id
        self.number = number
        self.name = name
        self.addresses = addresses if addresses else []
        self.date_of_foundation = date_of_foundation
        self.only_leaders = only_leaders
        self.show_members_improved = show_members_improved
        self.bank_account = bank_account
        self.email = email
        self.website = website
        self.info = info
        self.type = type
        self.contacts = contacts if contacts else []
        self.links = links if links else []

    def __str__(self):
        return "group_admin_id({}), number({}), name({}), addresses({}), date_of_foundation({}), only_leaders({}), show_member_improved({}), bank_account({}), email({}), website({}), info({}), type({}), contacts({}), links({})".format(
            self.group_admin_id,
            self.number,
            self.name,
            ", ".join(str(address) for address in self.addresses),
            self.date_of_foundation,
            self.only_leaders,
            self.show_members_improved,
            self.bank_account,
            self.email,
            self.website,
            self.info,
            self.type,
            ", ".join(str(contact) for contact in self.contacts),
            ", ".join(str(link) for link in self.links),
        )
