from datetime import datetime

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

from apps.members.models import Member
from apps.insurances.models import InsuranceType
from apps.insurances.models.enums import InsuranceStatus

from groupadmin.models import ScoutsGroup, ScoutsAddress


class BaseInsuranceQuerySet(models.QuerySet):
    def allowed(self, user: settings.AUTH_USER_MODEL):
        user_group_ids = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(_group_group_admin_id__in=user_group_ids)

    def editable(self):
        return self.filter(_status__in=[InsuranceStatus.NEW, InsuranceStatus.WAITING])


class BaseInsuranceManager(models.Manager):
    def get_queryset(self):
        return BaseInsuranceQuerySet(self.model, using=self._db)


class BaseInsurance(models.Model):
    objects = BaseInsuranceManager()

    id = models.AutoField(primary_key=True, db_column="verzekeringsid")
    _status = models.IntegerField(db_column="status", null=True, blank=True)
    invoice_number = models.IntegerField(db_column="factuurnr", null=True, blank=True)
    invoice_date = models.DateTimeField(db_column="facturatiedatum", null=True, blank=True)

    _group_group_admin_id = models.CharField(db_column="groepsnr", max_length=6)
    _group_name = models.CharField(db_column="groepsnaam", max_length=50)
    _group_location = models.CharField(db_column="groepsplaats", max_length=50)

    total_cost = models.DecimalField(db_column="totkostprijs", null=True, max_digits=7, decimal_places=2)
    comment = models.CharField(db_column="opmerking", max_length=500, blank=True)
    vvks_comment = models.CharField(db_column="vvksmopmerking", max_length=500, blank=True)

    _printed = models.CharField(db_column="afgedrukt", max_length=1, default="N")
    _finished = models.CharField(db_column="afgewerkt", max_length=1, default="N")
    _listed = models.CharField(db_column="lijstok", max_length=1, default="N")

    created_on = models.DateTimeField(db_column="datumvaninvulling", null=True)
    _start_date = models.DateTimeField(db_column="begindatum", null=True)
    _end_date = models.DateTimeField(db_column="einddatum", null=True)
    payment_date = models.DateTimeField(db_column="betalingsdatum", null=True, blank=True)

    responsible_member = models.ForeignKey(Member, db_column="verantwoordelijkeid", on_delete=models.CASCADE)
    type = models.ForeignKey(InsuranceType, null=True, db_column="typeid", on_delete=models.RESTRICT)

    class Meta:
        db_table = "vrzkverzekeringen"
        managed = False

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date needs to be before or equal to end date")

    # Utility functions for parsing char boolean to actual boolean and the reverse
    def parse_bool_to_char(value: bool) -> str:
        if value:
            return "J"
        else:
            return "N"

    def parse_char_to_bool(value: str) -> bool:
        if value == "J":
            return True
        else:
            return False

    # Special group getter that returns group class to make it seem like normal model
    @property
    def group(self):
        return ScoutsGroup(
            group_admin_id=self._group_group_admin_id,
            name=self._group_name,
            addresses=[ScoutsAddress(city=self._group_location)],
        )

    # Special group setter that accepts group class
    @group.setter
    def group(self, value: ScoutsGroup):
        self._group_group_admin_id = value.group_admin_id
        self._group_name = value.name
        self._group_location = value.addresses[0].city

    # Parse status int to actual string
    @property
    def status(self):
        return InsuranceStatus(self._status)

    @status.setter
    def status(self, value):
        self._status = value.value

    def is_accepted(self):
        return self.status == InsuranceStatus.ACCEPTED or self.status == InsuranceStatus.BILLED

    # Create property getter and setters for the boolean charfields so we can use them properly
    @property
    def printed(self):
        return self.parse_char_to_bool(self._printed)

    @printed.setter
    def printed(self, value):
        self._printed = self.parse_bool_to_char(value)

    @property
    def finished(self):
        return self.parse_char_to_bool(self._finished)

    @finished.setter
    def finished(self, value):
        self._finished = self.parse_bool_to_char(value)

    @property
    def listed(self):
        return self.parse_char_to_bool(self._listed)

    @listed.setter
    def listed(self, value):
        self._listed = self.parse_bool_to_char(value)

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value: datetime.date):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value: datetime.date):
        self._end_date = value

    @property
    def editable(self):
        return self.status in [InsuranceStatus.NEW, InsuranceStatus.WAITING]
