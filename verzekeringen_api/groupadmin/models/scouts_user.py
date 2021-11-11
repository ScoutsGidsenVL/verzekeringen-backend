from typing import List
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
    scouts_groups: List[ScoutsGroup]
    addresses: List[ScoutsAddress]
    functions: List[ScoutsFunction]
    group_specific_fields: List[ScoutsGroupSpecificField]
    links: List[ScoutsLink]

    #
    # The active access token, provided by group admin oidc
    #
    access_token: str = ""
