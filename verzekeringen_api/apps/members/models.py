import logging
from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError

from apps.members.managers import InuitsNonMemberManager

from inuits.models import Gender, GenderHelper

from groupadmin.models import PostcodeCity


logger = logging.getLogger(__name__)


class AbstractMember(models.Model):

    last_name = models.CharField(db_column="naam", max_length=25)
    first_name = models.CharField(db_column="voornaam", max_length=15)
    phone_number = models.CharField(db_column="telefoon", max_length=15, blank=True)
    _birth_date = models.DateField(db_column="geboortedatum", null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    # Because of the old database Datefields return as datetime, fix this
    @property
    def birth_date(self):
        if type(self._birth_date) == datetime:
            return self._birth_date.date()
        return self._birth_date

    @birth_date.setter
    def birth_date(self, value: datetime.date):
        self._birth_date = value


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
            raise ValidationError("Birth date, Phone number and email need to be either filled in or blank together")


class NonMember(AbstractMember, models.Model):

    id = models.AutoField(db_column="nietlidid", primary_key=True)
    street = models.CharField(db_column="straat", max_length=100, blank=True)
    number = models.CharField(db_column="nr", max_length=5, blank=True)
    letter_box = models.CharField(db_column="bus", max_length=5, blank=True)
    postcode = models.IntegerField(db_column="postcode", null=True, blank=True)
    city = models.CharField(db_column="gemeente", max_length=40, blank=True)
    comment = models.CharField(db_column="commentaar", max_length=500, blank=True)

    class Meta:
        db_table = "vrzknietleden"
        managed = False
        ordering = ["id"]

    def clean(self):
        if not (self.street and self.number and self.postcode and self.city) or (
            not self.street and not self.number and not self.postcode and not self.city
        ):
            raise ValidationError("Street, number, postcode and city need to be either filled in or blank together")

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)


class InuitsNonMember(models.Model):
    """
    Extra non member class we can use to save unique non members so
    we can have an easy and clean table to search in.
    These are not linked to any insurance but just used to offer some extra
    functionalities that old database doesnt allow us to do.
    """

    objects = InuitsNonMemberManager()

    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=15)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=5)
    letter_box = models.CharField(max_length=5, blank=True)
    # Making postcode int field is bad practice but keeping it because of compatibility with actual NonMember
    postcode = models.IntegerField()
    city = models.CharField(max_length=40)
    comment = models.CharField(max_length=500, blank=True)
    # Keep group number
    group_group_admin_id = models.CharField(max_length=6)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=Gender.choices, default=Gender.UNKNOWN)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)

    @property
    def address(self):
        return Address(
            street=self.street, number=self.number, letter_box=self.letter_box, postcode=self.postcode, city=self.city
        )

    @property
    def get_gender(self):
        gender = GenderHelper.parse_gender(self.gender)

        return gender


class Address(models.Model):

    id = models.AutoField(db_column="adres_id", primary_key=True)
    street = models.CharField(db_column="straat", max_length=100)
    number = models.CharField(db_column="nummer", max_length=5)
    letter_box = models.CharField(db_column="bus", max_length=5, null=True, blank=True)
    postcode = models.CharField(db_column="postcode", max_length=4)
    city = models.CharField(db_column="gemeente", max_length=40)

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)

    class Meta:
        db_table = "vrzk_adres"
        managed = False


class NonMemberInuitsTemplate(models.Model):
    non_member = models.OneToOneField(
        NonMember, on_delete=models.CASCADE, primary_key=True, db_constraint=models.UniqueConstraint
    )
    inuits_non_member = models.ForeignKey(InuitsNonMember, on_delete=models.CASCADE)

    def get_gender(self):
        return self.inuits_non_member.get_gender()
