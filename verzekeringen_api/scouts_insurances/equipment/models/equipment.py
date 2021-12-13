from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from scouts_insurances.people.models import Member, NonMember
from scouts_insurances.insurances.models import EquipmentInsurance


class Equipment(models.Model):

    id = models.AutoField(db_column="materiaalid", primary_key=True)
    nature = models.CharField(db_column="aard", max_length=50, blank=True)
    description = models.CharField(db_column="materieomschrijving", max_length=500)
    # Amount will not be used in the future so we will put it default 1 and ignore it
    amount = models.IntegerField(db_column="aantal", validators=[MinValueValidator(1)], default=1)
    total_value = models.DecimalField(
        db_column="nieuwwaardeperstuk",
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    insurance = models.ForeignKey(
        EquipmentInsurance,
        null=True,
        db_column="verzekeringsid",
        related_name="equipment",
        on_delete=models.CASCADE,
    )
    owner_non_member = models.ForeignKey(
        NonMember,
        null=True,
        related_name="equipment",
        db_column="eigenaaridnietlid",
        blank=True,
        on_delete=models.CASCADE,
    )
    owner_member = models.ForeignKey(
        Member,
        null=True,
        related_name="equipment",
        db_column="eigenaaridlid",
        blank=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "vrzkmateriaal"
        managed = False

    def clean(self):
        if self.owner_non_member and self.owner_member:
            raise ValidationError("There needs to be only one owner")
        if self.owner_member and self.nature:
            raise ValidationError("If the equipment owner is a member then equipment nature can not be given")
