import logging
from datetime import datetime

from django.db import models

from scouts_auth.inuits.models.fields import DatetypeAwareDateField


logger = logging.getLogger(__name__)


class AbstractMember(models.Model):

    last_name = models.CharField(db_column="naam", max_length=25)
    first_name = models.CharField(db_column="voornaam", max_length=15)
    phone_number = models.CharField(db_column="telefoon", max_length=15, blank=True)
    birth_date = DatetypeAwareDateField(db_column="geboortedatum", null=True, blank=True)

    class Meta:
        abstract = True

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    # Because of the old database Datefields return as datetime, fix this
    # @property
    # def birth_date(self):
    #     if isinstance(self._birth_date, datetime):
    #         logger.debug("DATETIME INSTANCE for %s %s", self.first_name, self.last_name)
    #         return self._birth_date.date()
    #     return self._birth_date

    # @birth_date.setter
    # def birth_date(self, value):
    #     if isinstance(value, datetime):
    #         logger.debug("DATETIME INSTANCE on setter for %s %s", self.first_name, self.last_name)
    #         self._birth_date = value.date()
    #     else:
    #         self._birth_date = value

    def __str__(self):
        return "first_name({}), last_name({}), phone_number({}), birth_date({})".format(
            self.first_name, self.last_name, self.phone_number, self.birth_date
        )
