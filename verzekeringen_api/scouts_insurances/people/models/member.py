import logging

from django.core.exceptions import ValidationError
from django.db import models

from scouts_insurances.people.models import AbstractMember

logger = logging.getLogger(__name__)


class Member(AbstractMember, models.Model):

    id = models.AutoField(db_column="lidid", primary_key=True)
    membership_number = models.BigIntegerField(db_column="lidnr")
    email = models.EmailField(max_length=60, blank=True)
    group_admin_id = models.CharField(db_column="ga_id", max_length=255, blank=True)

    class Meta:
        db_table = "vrzkleden"
        managed = False
        ordering = ["id"]

    def clean(self):
        if not (self.birth_date and self.phone_number and self.email) or (
            not self.birth_date and not self.phone_number and not self.email
        ):
            raise ValidationError("Birth date, phone number and email need to be either filled in or blank together")

    def __str__(self):
        return "{}, group_admin_id({}), membership_number({})".format(
            super().__str__(), self.group_admin_id, self.membership_number
        )

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)
