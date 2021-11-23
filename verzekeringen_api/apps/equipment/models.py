from datetime import datetime
from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from apps.members.models import Member, NonMember, InuitsNonMember
from apps.equipment.enums import VehicleType, VehicleTrailerOption
from apps.equipment.managers import InuitsVehicleManager, InuitsEquipmentManager
from apps.insurances.models import TemporaryVehicleInsurance


class Equipment(models.Model):

    id = models.AutoField(db_column="materiaalid", primary_key=True)
    nature = models.CharField(db_column="aard", max_length=50, blank=True)
    description = models.CharField(db_column="materieomschrijving", max_length=500)
    # Amount will not be used in the future so we will put it default 1 and ignore it
    _amount = models.IntegerField(db_column="aantal", validators=[MinValueValidator(1)], default=1)
    total_value = models.DecimalField(
        db_column="nieuwwaardeperstuk",
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    insurance = models.ForeignKey(
        "insurances.EquipmentInsurance",
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
            raise ValidationError("If owner member then nature can not be given")


class InuitsEquipment(models.Model):
    objects = InuitsEquipmentManager()

    id = models.AutoField(primary_key=True)
    nature = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=500)
    # Amount will not be used in the future so we will put it default 1 and ignore it
    _amount = models.IntegerField(validators=[MinValueValidator(1)], default=1)
    total_value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    owner_non_member = models.ForeignKey(
        InuitsNonMember,
        null=True,
        related_name="inuits_equipment",
        blank=True,
        on_delete=models.CASCADE,
    )
    # Save some group admin id of owner, all detailed info will be gotten from group admin
    owner_member_group_admin_id = models.CharField(db_column="ga_id", max_length=255, blank=True, null=True)
    # GroupAdmin id of the group to which the equipment belongs
    owner_group_group_admin_id = models.CharField(max_length=6)

    def clean(self):
        if self.owner_non_member and self.owner_member_group_admin_id:
            raise ValidationError("There needs to be only one owner")
        if self.owner_member_group_admin_id and self.nature:
            raise ValidationError("If owner member then nature can not be given")
        if not self.owner_non_member and not self.owner_member_group_admin_id and not self.owner_group_group_admin_id:
            raise ValidationError("A piece of equipment needs to have an owner")


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
    trailer = models.CharField(choices=VehicleTrailerOption.choices, max_length=1, default="0")

    # GroupAdmin id of the group to which the vehicle belongs
    group_group_admin_id = models.CharField(max_length=6)

    class Meta:
        constraints = [
            # add unique constraint on chassis_number
        ]

    def clean_construction_year(self, value):
        if datetime.strptime("1900", "%Y") > value:
            raise ValidationError("Invalid construction year")
        return value


class VehicleInuitsTemplate(models.Model):
    temporary_vehicle_insurance = models.OneToOneField(
        TemporaryVehicleInsurance, on_delete=models.CASCADE, primary_key=True, db_constraint=models.UniqueConstraint
    )
    inuits_vehicle = models.ForeignKey(InuitsVehicle, on_delete=models.CASCADE)


class EquipmentInuitsTemplate(models.Model):
    equipment = models.OneToOneField(
        Equipment, on_delete=models.CASCADE, primary_key=True, db_constraint=models.UniqueConstraint
    )
    inuits_equipment = models.ForeignKey(InuitsEquipment, on_delete=models.CASCADE)
