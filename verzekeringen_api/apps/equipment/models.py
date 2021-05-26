from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.members.models import Member, NonMember

# from apps.insurances.models import Insurance


class Equipment(models.Model):

    id = models.AutoField(db_column="materiaalid", primary_key=True)
    nature = models.CharField(db_column="aard", max_length=50, blank=True)
    description = models.CharField(db_column="materieomschrijving", max_length=500)
    amount = models.IntegerField(db_column="aantal", null=True, blank=True, validators=[MinValueValidator(1)])
    new_value = models.DecimalField(
        db_column="nieuwwaardeperstuk",
        null=True,
        blank=True,
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    # insurance = models.ForeignKey(Insurance, null=True, db_column="verzekeringsid")
    owner_non_member = models.ForeignKey(
        NonMember, null=True, related_name="equipment", db_column="eigenaaridnietlid", blank=True
    )
    owner_member = models.ForeignKey(
        Member, null=True, related_name="equipment", db_column="eigenaaridlid", blank=True
    )

    class Meta:
        db_table = "vrzkmateriaal"
        managed = False

    def clean(self):
        pass
        # if self.owner_non_member and not self.nature:
        #     raise ValidationError("If owner member then nature can not be given")
        # if not self.owner_non_member and self.nature:
        #     raise ValidationError("If no owner member then nature can not be given")
