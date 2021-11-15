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

    def __str__(self):
        return "group_admin_id({}), ".format(self.group_admin_id) + super().__str__()

    def get_function_codes(self) -> List[str]:
        return [function.code for function in self.functions]

    def get_group_functions(self) -> List[Tuple]:
        return [(function.group.group_admin_id, function.code) for function in self.functions]

    @property
    def is_administrator(self) -> bool:
        return any(
            name in [group.group_admin_id for group in self.scouts_groups]
            for name in SettingsHelper.get_administrator_groups()
        )

    @property
    def is_district_commissioner(self) -> bool:
        for function in self.functions:
            if function.is_district_commissioner():
                return True
        return False

    def is_group_leader(self, group: ScoutsGroup) -> bool:
        for function in self.functions:
            if function.is_group_leader():
                self.group_leader = True
                break
        return self.group_leader

    def is_leader(self, group: ScoutsGroup) -> bool:
        for function in self.functions:
            if function.is_leader():
                self.leader = True
                break
        return self.leader
