from django.db import models
from django.core.exceptions import ValidationError

from scouts_insurances.locations.models import Country

from scouts_insurances.people.models import NonMember
from scouts_insurances.insurances.models import BaseInsurance


class TemporaryInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="temporary_child",
    )
    nature = models.CharField(db_column="aardactiviteit", max_length=500)
    postal_code = models.IntegerField(db_column="postcode", null=True, blank=True)
    city = models.CharField(db_column="gemeente", max_length=40, blank=True)
    _country = models.CharField(db_column="land", max_length=60, blank=True)

    non_members = models.ManyToManyField(
        NonMember, through="NonMemberTemporaryInsurance", related_name="temporary_insurances"
    )

    class Meta:
        db_table = "vrzktypetijdact"
        managed = False

    def clean(self):
        super().clean()
        if self._country and (self.postal_code or self.city):
            raise ValidationError("If country given then postal code and city cannot be given")
        elif not self.country and ((self.postal_code and not self.city) or (self.city and not self.postal_code)):
            raise ValidationError("When no country given both city and postal_code are required")

    @property
    def country(self) -> Country:
        if self._country:
            return Country.objects.by_name(self._country)
        return None

    @country.setter
    def country(self, country: str):
        self._country = country

    @country.setter
    def country(self, value):
        if isinstance(value, Country):
            self._country = value.name
        else:
            self._country = value
