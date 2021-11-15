from django.db import models
from django.core.exceptions import ValidationError
from apps.locations.models import Country
from apps.locations.utils import PostcodeCity
from apps.insurances.models.base_insurance import BaseInsurance


class EquipmentInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="equipment_child",
    )
    nature = models.CharField(db_column="aardactiviteit", max_length=500)
    postcode = models.IntegerField(db_column="postcode", null=True, blank=True)
    city = models.CharField(db_column="gemeente", max_length=40, blank=True)
    _country = models.CharField(db_column="land", max_length=45, blank=True)

    # Related Many field
    #
    # equipment (Equipment)

    class Meta:
        db_table = "vrzktypemateriaal"
        managed = False

    def clean(self):
        super().clean()
        if self._country and (self.postcode or self.city):
            raise ValidationError("If country given then postcode and city cannot be given")
        elif not self._country and ((self.postcode and not self.city) or (self.city and not self.postcode)):
            raise ValidationError("When no country given both city and postcode are required")

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)

    @property
    def country(self):
        return Country.objects.get(name=self._country)

    @country.setter
    def country(self, value: Country):
        if not value:
            self._country = None
        else:
            self._country = value.name
