from typing import List, Tuple
from datetime import date

from django.db import models

from scouts_auth.models import User

from groupadmin.models import (
    ScoutsAddress,
    ScoutsFunction,
    ScoutsGroupSpecificField,
    ScoutsLink,
    ScoutsGroup,
)
from groupadmin.utils import SettingsHelper

from inuits.models import Gender


class ScoutsUser(User):

    #
    # Fields from the groupadmin member record
    #
    group_admin_id: str = models.CharField(max_length=48, db_column="ga_id", blank=True)
    gender: Gender = models.CharField(max_length=16, choices=Gender.choices, default=Gender.UNKNOWN)
    phone_number: str = models.CharField(max_length=48, blank=True)
    membership_number: str = models.CharField(max_length=48, blank=True)
    customer_number: str = models.CharField(max_length=48, blank=True)
    birth_date: date = models.DateField(blank=True, null=True)

    #
    # Fields inherited from scouts_auth.models.User that may need to be updated after a call to groupadmin
    #
    # first_name = models.CharField(max_length=124, blank=True)
    # last_name = models.CharField(max_length=124, blank=True)
    # email = models.EmailField(blank=True)

    #
    # Locally cached, non-persisted fields
    #
    scouts_groups: List[ScoutsGroup] = []
    addresses: List[ScoutsAddress] = []
    functions: List[ScoutsFunction] = []
    group_specific_fields: List[ScoutsGroupSpecificField] = []
    links: List[ScoutsLink] = []

    #
    # The active access token, provided by group admin oidc
    #
    access_token: str = ""

    #
    # Some shortcut fields
    #
    is_administrator = False
    is_district_commissioner = False

    def __str__(self):
        return "group_admin_id({}), ".format(self.group_admin_id) + super().__str__()

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    def get_group_functions(self) -> List[Tuple]:
        return [(function.group.group_admin_id, function.code) for function in self.functions]

    def get_group_names(self) -> List[str]:
        return [group.group_admin_id for group in self.scouts_groups]

    def has_role_section_leader(self, group: ScoutsGroup) -> bool:
        """
        Determines if the user is a section leader based on a function in the specified group
        """
        for function in self.functions:
            if function.is_section_leader(group):
                return True
        return False

    def get_section_leader_groups(self) -> List[ScoutsGroup]:
        return [group for group in self.scouts_groups if self.has_role_section_leader(group)]

    def has_role_group_leader(self, group: ScoutsGroup) -> bool:
        """
        Determines if the user is a group leader based on a function in the specified group
        """
        for function in self.functions:
            if function.is_group_leader(group):
                return True
        return False

    def get_group_leader_groups(self) -> List[ScoutsGroup]:
        return [group for group in self.scouts_groups if self.has_role_group_leader(group)]

    def has_role_district_commissioner(self) -> bool:
        """
        Determines if the user is a district commissioner based on a function code
        """
        for function in self.functions:
            if function.is_district_commissioner():
                return True
        return False

    def has_role_administrator(self) -> bool:
        """
        Determines if the user as an administrative worker based on membership of an administrative group
        """
        if any(name in self.get_group_names() for name in SettingsHelper.get_administrator_groups()):
            self.is_administrator = True
        return self.is_administrator

    @property
    def permissions(self):
        return self.get_all_permissions()

    def __str__(self):
        return (
            super().__str__()
            + "group_admin_id({}), gender ({}), phone_number({}), membership_number({}), customer_number({}), birth_date({}), scouts_groups({}), addresses({}), functions({}), group_specific_fields({}), links({})"
        ).format(
            self.group_admin_id,
            self.gender,
            self.phone_number,
            self.membership_number,
            self.customer_number,
            self.birth_date,
            ", ".join(group.group_admin_id for group in self.scouts_groups),
            ", ".join(address.to_descriptive_string() for address in self.addresses),
            ", ".join(function.to_descriptive_string() for function in self.functions),
        )

    def to_descriptive_string(self):
        return (
            "{:<24}: {}\n"  # title
            "{:<24}: {}\n"  # username
            "{:<24}: {}\n"  # first_name
            "{:<24}: {}\n"  # last_name
            "{:<24}: {}\n"  # gender
            "{:<24}: {}\n"  # birth_date
            "{:<24}: {}\n"  # phone_number
            "{:<24}: {}\n"  # email
            "{:<24}: {}\n"  # group_admin_id
            "{:<24}: {}\n"  # membership_number
            "{:<24}: {}\n"  # customer_number
            "{:<24}: {}\n"  # addresses
            "{:<24}: {}\n"  # functions
            "{:<24}: {}\n"  # permissions
            "{:<24}: {}\n"  # auth groups
            "{:<24}: {}\n"  # scouts groups
            "{:<24}: {}\n"  # administrator ?
            "{:<24}: {}\n"  # district commissioner ?
            "{:<24}: {}\n"  # group leader
            "{:<24}: {}\n"  # section leader
        ).format(
            "USER INFO FOR",
            self.username,
            "username",
            self.username,
            "first_name",
            self.first_name,
            "last_name",
            self.last_name,
            "gender",
            self.gender,
            "birth_date",
            self.birth_date,
            "phone_number",
            self.phone_number,
            "email",
            self.email,
            "group_admin_id",
            self.group_admin_id,
            "membership_number",
            self.membership_number,
            "customer_number",
            self.customer_number,
            "addresses",
            " || ".join(address.to_descriptive_string() for address in self.addresses),
            "functions",
            " || ".join(function.to_descriptive_string() for function in self.functions),
            "PERMISSIONS",
            ", ".join(permission for permission in self.get_all_permissions()),
            "AUTH GROUPS",
            ", ".join(group.name for group in self.groups.all()),
            "SCOUTS GROUPS",
            ", ".join((group.name + "(" + group.group_admin_id + ")") for group in self.scouts_groups),
            "ADMINISTRATOR ?",
            self.has_role_administrator(),
            "DISTRICT COMMISSIONER ?",
            self.has_role_district_commissioner(),
            "GROUP LEADER",
            ", ".join(group.group_admin_id for group in self.get_group_leader_groups()),
            "SECTION LEADER",
            ", ".join(group.group_admin_id for group in self.get_section_leader_groups()),
        )
