from datetime import datetime

from django.db import models
from django.core.exceptions import ValidationError


from scouts_insurances.people.models import Member
from scouts_insurances.insurances.models import InsuranceType
from scouts_insurances.insurances.models.enums import InsuranceStatus
from scouts_insurances.insurances.managers import BaseInsuranceManager

from scouts_auth.groupadmin.models import ScoutsGroup, ScoutsAddress
from scouts_auth.inuits.models.fields import TimezoneAwareDateTimeField
from scouts_auth.inuits.utils import BooleanParser


class BaseInsurance(models.Model):
    objects = BaseInsuranceManager()

    id = models.AutoField(primary_key=True, db_column="verzekeringsid")
    _status = models.IntegerField(db_column="status", null=True, blank=True)
    invoice_number = models.IntegerField(db_column="factuurnr", null=True, blank=True)
    invoice_date = TimezoneAwareDateTimeField(db_column="facturatiedatum", null=True, blank=True)

    _group_group_admin_id = models.CharField(db_column="groepsnr", max_length=6)
    _group_name = models.CharField(db_column="groepsnaam", max_length=50)
    _group_location = models.CharField(db_column="groepsplaats", max_length=50)

    total_cost = models.DecimalField(db_column="totkostprijs", null=True, max_digits=7, decimal_places=2)
    comment = models.CharField(db_column="opmerking", max_length=500, blank=True)
    vvksm_comment = models.CharField(db_column="vvksmopmerking", max_length=500, blank=True)

    _printed = models.CharField(db_column="afgedrukt", max_length=1, default="N")
    _finished = models.CharField(db_column="afgewerkt", max_length=1, default="N")
    _listed = models.CharField(db_column="lijstok", max_length=1, default="N")

    created_on = TimezoneAwareDateTimeField(db_column="datumvaninvulling", null=True)
    _start_date = TimezoneAwareDateTimeField(db_column="begindatum", null=True)
    _end_date = TimezoneAwareDateTimeField(db_column="einddatum", null=True)
    payment_date = TimezoneAwareDateTimeField(db_column="betalingsdatum", null=True, blank=True)

    responsible_member = models.ForeignKey(Member, db_column="verantwoordelijkeid", on_delete=models.CASCADE)
    type = models.ForeignKey(InsuranceType, null=True, db_column="typeid", on_delete=models.RESTRICT)

    class Meta:
        db_table = "vrzkverzekeringen"
        managed = False

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Start date needs to be before or equal to end date")

    # Special group getter that returns group class to make it seem like normal model
    @property
    def scouts_group(self) -> ScoutsGroup:
        return ScoutsGroup(
            group_admin_id=self._group_group_admin_id,
            name=self._group_name,
            addresses=[ScoutsAddress(city=self._group_location)],
        )

    # Special group setter that accepts group class
    @scouts_group.setter
    def scouts_group(self, value: ScoutsGroup):
        self._group_group_admin_id = value.group_admin_id
        self._group_name = value.name
        self._group_location = value.addresses[0].city

    # Parse status int to actual string
    @property
    def status(self) -> InsuranceStatus:
        return InsuranceStatus(self._status)

    @status.setter
    def status(self, value: InsuranceStatus):
        self._status = value.value

    @property
    def editable(self) -> bool:
        """Determines if the insurance can still be edited (i.e. not yet accepted or billed or rejected)"""
        return self.status in [InsuranceStatus.NEW, InsuranceStatus.WAITING]

    @property
    def accepted(self) -> bool:
        """Determines if the insurance has been approved or billed (i.e. no longer editable or rejected)"""
        return self.status == InsuranceStatus.ACCEPTED or self.status == InsuranceStatus.BILLED

    # Create property getter and setters for the boolean charfields so we can use them properly
    @property
    def printed(self) -> bool:
        return BooleanParser.to_bool(self._printed)

    @printed.setter
    def printed(self, value: bool):
        self._printed = BooleanParser.to_char(value, "J", "N")

    @property
    def finished(self) -> bool:
        return BooleanParser.to_bool(self._finished)

    @finished.setter
    def finished(self, value: bool):
        self._finished = BooleanParser.to_char(value, "J", "N")

    @property
    def listed(self) -> bool:
        return BooleanParser.to_bool(self._listed)

    @listed.setter
    def listed(self, value: bool):
        self._listed = BooleanParser.to_char(value, "J", "N")

    @property
    def start_date(self) -> datetime:
        return self._start_date

    @start_date.setter
    def start_date(self, value: datetime):
        self._start_date = value

    @property
    def end_date(self) -> datetime:
        return self._end_date

    @end_date.setter
    def end_date(self, value: datetime):
        self._end_date = value

    def has_attachment(self) -> bool:
        """Provides a test on all insurances to see if there are attachments. Only some insurance types have attachments."""
        return False

    def __str__(self) -> str:
        return """id({}), type({}), status({}),total_cost({}), 
        start_date({}), end_date({}), 
        scouts_group({}), responsible_member({}), comment({}), vvksm_comment({}), 
        created_on({}),  
        printed({}), finished({}), listed({}), 
        invoice_number({}), invoice_date({}), payment_date({})""".format(
            self.id,
            self.type,
            self.status.label,
            self.total_cost,
            self.start_date,
            self.end_date,
            self.scouts_group.to_simple_string(),
            self.responsible_member,
            self.comment,
            self.vvksm_comment,
            self.created_on,
            self.printed,
            self.finished,
            self.listed,
            self.invoice_number,
            self.invoice_date,
            self.payment_date,
        )
