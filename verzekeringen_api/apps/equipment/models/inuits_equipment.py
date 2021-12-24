from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

from apps.equipment.managers import InuitsEquipmentManager
from apps.people.models import InuitsNonMember

from scouts_auth.groupadmin.models import AbstractScoutsGroup
from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsEquipment(AuditedBaseModel):
    """
    Extra class to model Equipment in the scouts tables.

    The jointable is defined in InuitsEquipmentTemplate
    """

    objects = InuitsEquipmentManager()

    nature = OptionalCharField(max_length=50, null=True)
    description = models.CharField(max_length=500)
    # Amount will not be used in the future so we will put it default 1 and ignore it
    amount = models.IntegerField(validators=[MinValueValidator(1)], default=1)
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
    # Save group admin id of owner member, all detailed info will be gotten from group admin
    owner_member = OptionalCharField(max_length=255, null=True)
    # The group admin id of the group to which the equipment belongs
    owner_group = OptionalCharField(max_length=6, null=True)

    def clean(self):
        # if self.owner_member and self.nature:
        #     raise ValidationError("If owner member then nature can not be given")
        if self.owner_non_member and self.owner_member:
            raise ValidationError("There needs to be only one owner")
        if not self.owner_non_member and not self.owner_member and not self.owner_group:
            raise ValidationError("A piece of equipment needs to have an owner")

    def has_id(self):
        return self.id is not None

    def equals(self, instance) -> bool:
        return (
            instance is not None
            and type(instance).__name__ == "InuitsEquipment"
            and self.nature == instance.nature
            and self.description == instance.description
            and self.amount == instance.amount
            and self.total_value == instance.total_value
            and self.owner_non_member == instance.owner_non_member
            and self.owner_member == instance.owner_member
            and self.owner_group == instance.owner_group
        )

    def __str__(self):
        return "id({}), nature({}), description({}), amount({}), total_value({}), owner_non_member({}), owner_member({}), owner_group({})".format(
            self.id,
            self.nature,
            self.description,
            self.amount,
            self.total_value,
            self.owner_non_member.id if self.owner_non_member else "",
            self.owner_member.group_admin_id if self.owner_member else "",
            self.owner_group.group_admin_id
            if self.owner_group and isinstance(self.owner_group, AbstractScoutsGroup)
            else self.owner_group
            if self.owner_group
            else "",
        )
