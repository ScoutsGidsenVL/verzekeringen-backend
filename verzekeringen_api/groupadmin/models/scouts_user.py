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
    phone: str = models.CharField(max_length=48, blank=True)
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

    def has_role_administrator(self) -> bool:
        if any(name in self.get_group_names() for name in SettingsHelper.get_administrator_groups()):
            self.is_administrator = True
        return self.is_administrator

    def has_role_district_commissioner(self) -> bool:
        for function in self.functions:
            if function.is_district_commissioner():
                self.is_district_commissioner = True
                break
        return self.is_district_commissioner

    def is_group_leader(self, group: ScoutsGroup) -> bool:
        for function in self.functions:
            if function.is_group_leader() and function.group.group_admin_id == group.group_admin_id:
                return True
        return False

    def is_leader(self, group: ScoutsGroup) -> bool:
        for function in self.functions:
            if function.is_leader() and function.group.group_admin_id == group.group_admin_id:
                return True
        return False
