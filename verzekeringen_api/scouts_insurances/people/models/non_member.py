import logging

from django.db import models
from django.core.exceptions import ValidationError

from scouts_insurances.people.managers import NonMemberManager
from scouts_insurances.people.models import AbstractMember


logger = logging.getLogger(__name__)


class NonMember(AbstractMember, models.Model):
    # FIELDS INHERITED FROM ABSTRACTMEMBER
    # first_name    max_length=15       required
    # last_name     max_length=25       required
    # phone_number  max_length=15       optional
    # birth_date    date                optional

    objects = NonMemberManager()

    id = models.AutoField(db_column="nietlidid", primary_key=True)
    street = models.CharField(db_column="straat", max_length=100, blank=True)
    number = models.CharField(db_column="nr", max_length=5, blank=True)
    letter_box = models.CharField(db_column="bus", max_length=5, blank=True)
    postal_code = models.IntegerField(db_column="postcode", null=True, blank=True)
    city = models.CharField(db_column="gemeente", max_length=40, blank=True)
    comment = models.CharField(db_column="commentaar", max_length=500, blank=True)

    class Meta:
        db_table = "vrzknietleden"
        managed = False
        ordering = ["id"]

    def clean(self):
        if not (self.street and self.number and self.postal_code and self.city) or (
            not self.street and not self.number and not self.postal_code and not self.city
        ):
            raise ValidationError("Street, number, postal code and city need to be either filled in or blank together")

    def __str__(self):
        return "id({}), {}, street({}), number({}), letter_box({}), postal_code({}), city({}), comment({})".format(
            self.id,
            self.abstract_member_to_str(),
            self.street,
            self.number,
            self.letter_box,
            self.postal_code,
            self.city,
            self.comment,
        )
