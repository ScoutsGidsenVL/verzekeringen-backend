from django.db import models

from scouts_insurances.locations.managers import CountryManager

from scouts_insurances.insurances.models import InsuranceType


class Country(models.Model):
    objects = CountryManager()

    DEFAULT_COUNTRY_NAME = "België"

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60, unique=True)
    insurance_types = models.ManyToManyField(InsuranceType, related_name="country_options")
