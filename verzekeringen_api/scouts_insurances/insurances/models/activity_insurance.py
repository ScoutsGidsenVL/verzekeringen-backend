from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from scouts_insurances.insurances.models import BaseInsurance


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
    group_size = models.IntegerField(
        db_column="aantgroep", null=True, validators=[MinValueValidator(1), MaxValueValidator(9)]
    )
    postal_code = models.IntegerField(db_column="postcode", null=True)
    city = models.CharField(db_column="gemeente", max_length=40)

    class Meta:
        db_table = "vrzktypeeenact"
        managed = False

    def has_attachment(self) -> bool:
        return self.attachment is not None
