from django.db import models
from typing import Union

from apps.insurances.models.enums.insurance_claim import ActivityType, DamageType
from apps.members.enums import Sex
from apps.members.models import Member, InuitsNonMember
from apps.scouts_auth.models import User
from django.core.exceptions import ValidationError
from jsonfield import JSONField


class InsuranceClaim(models.Model):
    group_number = models.CharField(max_length=6, null=True)
    date = models.DateTimeField(blank=True)
    declarant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
    declarant_city = models.CharField(max_length=30, null=True, blank=True)
    legal_representative = models.CharField(max_length=128, null=True, blank=True)
    victim_member_group_admin_id = models.CharField(
        db_column="ga_id",
        max_length=255,
        blank=True,
        null=True)
    #
    victim_non_member = models.ForeignKey(
        InuitsNonMember,
        null=True,
        related_name="claim_victim",
        blank=True,
        on_delete=models.SET_NULL,
    )

    bank_account = models.CharField(max_length=30, null=True, blank=True)
    date_of_accident = models.DateTimeField()
    activity = models.CharField(max_length=1024)
    # Custom JSONField
    activity_type = JSONField(max_length=128)
    location = models.CharField(max_length=128, null=True, blank=True)
    used_transport = models.CharField(max_length=30, null=True, blank=True)
    damage_type = models.CharField(max_length=30, choices=DamageType.choices, null=True, blank=True)
    description = models.CharField(max_length=1024)

    involved_party_description = models.CharField(max_length=1024, null=True, blank=True)
    involved_party_birthdate = models.DateField(null=True, blank=True)

    official_report_description = models.CharField(max_length=1024, null=True, blank=True)
    pv_number = models.CharField(max_length=30, null=True, blank=True)

    witness_name = models.CharField(max_length=128, null=True, blank=True)
    witness_description = models.CharField(max_length=1024, null=True, blank=True)

    leadership_description = models.CharField(max_length=1024, null=True, blank=True)

    note = models.CharField(max_length=1024, null=True, blank=True)
    case_number = models.CharField(max_length=30, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=Sex.choices, default='O')

    def clean(self):
        if self.victim_non_member and self.victim_member_group_admin_id:
            raise ValidationError("There needs to be only one owner")

        if not self.victim_member_group_admin_id and not self.victim_non_member:
            raise ValidationError("At least one member have to be specified")

    def get_victim(self) -> Union[InuitsNonMember, str]:
        if self.victim_member_group_admin_id:
            return self.victim_member_group_admin_id
        return self.victim_non_member

