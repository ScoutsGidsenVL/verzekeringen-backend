from django.db import models

from groupadmin.models import ScoutsAddress

from inuits.models import Gender, AuditedBaseModel
from inuits.models.fields import OptionalCharField, DefaultCharField, OptionalIntegerField, OptionalDateField


class InuitsAbstractPerson(AuditedBaseModel):
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=25)
    phone_number = OptionalCharField(max_length=15)
    birth_date = OptionalDateField()
    gender = DefaultCharField(choices=Gender.choices, default=Gender.UNKNOWN, max_length=1)
    street = OptionalCharField(max_length=100)
    number = OptionalCharField(max_length=5)
    letter_box = OptionalCharField(max_length=5)
    postal_code = OptionalIntegerField()
    city = OptionalCharField(max_length=40)
    comment = OptionalCharField(max_length=500)
    email = OptionalCharField()

    _address: ScoutsAddress = None

    class Meta:
        abstract = True

    @property
    def address(self):
        if not self._address:
            self._address = ScoutsAddress(
                street=self.street,
                number=self.number,
                letter_box=self.letter_box,
                postal_code=self.postal_code,
                city=self.city,
            )
        return self._address
