from django.db import models


class Country(models.Model):

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    insurance_types = models.ManyToManyField("insurances.InsuranceType", related_name="country_options")
