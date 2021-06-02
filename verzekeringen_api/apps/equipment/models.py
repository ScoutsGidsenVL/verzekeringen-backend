from datetime import datetime
from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from apps.members.models import Member, NonMember
from .enums import VehicleType
from .managers import InuitsVehicleManager


# class Equipment(models.Model):

#     id = models.AutoField(db_column="materiaalid", primary_key=True)
#     nature = models.CharField(db_column="aard", max_length=50, blank=True)
#     description = models.CharField(db_column="materieomschrijving", max_length=500)
#     amount = models.IntegerField(db_column="aantal", null=True, blank=True, validators=[MinValueValidator(1)])
#     new_value = models.DecimalField(
#         db_column="nieuwwaardeperstuk",
#         null=True,
#         blank=True,
#         max_digits=7,
#         decimal_places=2,
#         validators=[MinValueValidator(Decimal("0.01"))],
#     )
#     # insurance = models.ForeignKey(Insurance, null=True, db_column="verzekeringsid")
#     # owner_non_member = models.ForeignKey(
#     #     NonMember, null=True, related_name="equipment", db_column="eigenaaridnietlid", blank=True
#     # )
#     # owner_member = models.ForeignKey(
#     #     Member, null=True, related_name="equipment", db_column="eigenaaridlid", blank=True
#     # )

#     class Meta:
#         db_table = "vrzkmateriaal"
#         managed = False

#     def clean(self):
#         pass
#         # if self.owner_non_member and not self.nature:
#         #     raise ValidationError("If owner member then nature can not be given")
#         # if not self.owner_non_member and self.nature:
#         #     raise ValidationError("If no owner member then nature can not be given")


class InuitsVehicle(models.Model):
    """Extra vehicle class we can use to save and search unique vehicles"""

    objects = InuitsVehicleManager()

    id = models.AutoField(primary_key=True)
    type = models.CharField(
        max_length=30,
        choices=VehicleType.choices,
    )
    brand = models.CharField(max_length=15)
    license_plate = models.CharField(max_length=10)
    construction_year = models.DateField()
    chassis_number = models.CharField(max_length=20)
    trailer = models.BooleanField(default=True)
    group_number = models.CharField(max_length=6)

    def clean_construction_year(self, value):
        if datetime.strptime("1900", "%Y") > value:
            raise ValidationError("Invalid construction year")
        return value
