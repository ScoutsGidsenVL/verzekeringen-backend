from django.db import models

from apps.insurances.models.enums.insurance_claim import ActivityType, DamageType
from apps.members.models import Member, InuitsNonMember
from apps.scouts_auth.models import User
from django.core.exceptions import ValidationError


class InsuranceClaim(models.Model):
    group_number = models.CharField(max_length=6, null=True)
    date = models.DateTimeField(blank=True)
    person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=False)
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
    activity_type = models.CharField(max_length=30, choices=ActivityType.choices)
    used_transport = models.CharField(max_length=30, null=True, blank=True)
    damage_type = models.CharField(max_length=30, choices=DamageType.choices, null=True, blank=True)
    description = models.CharField(max_length=1024)

    involved_party_description = models.CharField(max_length=1024, null=True, blank=True)
    involved_party_birthdate = models.DateField(null=True, blank=True)

    official_report_description = models.CharField(max_length=1024, null=True, blank=True)
    pv_number = models.CharField(max_length=30, null=True, blank=True)

    witness_description = models.CharField(max_length=1024, null=True, blank=True)

    leadership_description = models.CharField(max_length=1024, null=True, blank=True)

    def clean(self):
        if self.victim_non_member and self.victim_member_group_admin_id:
            raise ValidationError("There needs to be only one owner")

        if not self.victim_member_group_admin_id and not self.victim_non_member:
            raise ValidationError("At least one member have to be specified")
