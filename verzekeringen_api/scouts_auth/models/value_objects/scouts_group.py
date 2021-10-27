from typing import List
from datetime import date

from scouts_auth.models.value_objects import GroupAdminAddress, GroupAdminLink


class ScoutsGroupContact:

    member: str
    function: str
    name: str
    phone: str
    email: str
    links: List[GroupAdminLink]


class ScoutsGroup:
    """Models the scouts groups a user has rights to."""

    id: str
    name: str
    number: str
    addresses: List[GroupAdminAddress]
    date_of_foundation: date
    bank_account: str
    email: str
    website: str
    info: str
    contacts: List[ScoutsGroupContact]

    def __init__(
        self,
        id: str = None,
        name: str = None,
        number: str = None,
        addresses: List[GroupAdminAddress] = None,
        date_of_foundation: date = None,
        bank_account: str = None,
        email: str = None,
        website: str = None,
        info: str = None,
        contacts: List[ScoutsGroupContact] = None,
    ):
        self.id = id if id else ""
        self.name = name if name else ""
        self.number = number if number else ""
        self.addresses = addresses if addresses else []
        self.date_of_foundation = date_of_foundation
        self.bank_account = bank_account if bank_account else ""
        self.email = email if email else ""
        self.website = website if website else ""
        self.info = info if info else ""
        self.contacts = contacts if contacts else []
    
    def __str__(self):
        return ("% (%) - %") % (self.name, self.number, self.website)
