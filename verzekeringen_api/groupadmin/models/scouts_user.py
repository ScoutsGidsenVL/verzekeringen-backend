from typing import List
from datetime import date

from django.db import models

from groupadmin.models import (
    ScoutsAddress,
    ScoutsFunction,
    ScoutsGroupSpecificField,
    ScoutsLink,
    ScoutsGroup,
)

from inuits.models import Gender


class ScoutsUser:

    group_admin_id: str = models.CharField()
    username: str = models.CharField()
    first_name: str = models.CharField()
    last_name: str = models.CharField()
    birth_date: date = models.DateField()
    gender: Gender = models.TextChoices(choices=Gender.choices, default=Gender.UNKNOWN)
    phone: str = models.CharField()
    customer_number: str = models.CharField()
    membership_number: str = models.CharField
    email = models.EmailField()

    # Locally cached, non-persisted fields
    groups: List[ScoutsGroup]
    addresses: List[ScoutsAddress]
    functions: List[ScoutsFunction]
    group_specific_fields: List[ScoutsGroupSpecificField]
    links: List[ScoutsLink]
