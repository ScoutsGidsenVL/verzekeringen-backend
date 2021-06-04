from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.locations.utils import PostcodeCity
from .base_insurance import BaseInsurance
from .enums import GroupSize


class ActivityInsurance(BaseInsurance):
    insurance_parent = models.OneToOneField(
        BaseInsurance,
        db_column="verzekeringsid",
        on_delete=models.CASCADE,
        parent_link=True,
        primary_key=True,
        related_name="activity_child",
    )
    nature = models.CharField(db_column="aardactiviteit", max_length=500)
    _group_size = models.IntegerField(
        db_column="aantgroep", null=True, validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    postcode = models.IntegerField(db_column="postcode", null=True)
    city = models.CharField(db_column="gemeente", max_length=40)

    class Meta:
        db_table = "vrzktypeeenact"
        managed = False

    # Parse group_size int to enum
    @property
    def group_size(self):
        return GroupSize(self._group_size)

    @group_size.setter
    def group_size(self, value):
        self._group_size = value.value

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)
