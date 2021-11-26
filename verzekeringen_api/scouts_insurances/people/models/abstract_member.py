import logging
from datetime import datetime

from django.db import models


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
