from jsonfield import JSONField

from django.conf import settings
from django.db import models

from apps.people.models import InuitsClaimVictim
from apps.insurances.models.enums import ClaimActivityType
from apps.insurances.managers import InsuranceClaimManager

from scouts_auth.groupadmin.services import GroupAdmin

from scouts_auth.inuits.models import AuditedBaseModel
from scouts_auth.inuits.models.fields import (
    OptionalCharField,
    OptionalDateField,
    OptionalDateTimeField,
    OptionalForeignKey,
    RequiredCharField,
)


class InsuranceClaim(AuditedBaseModel):
    """Persists data related to an insurance claim."""

    objects = InsuranceClaimManager()

    # An accident is always filed in the context of a scouts group.
    group_group_admin_id = OptionalCharField(max_length=6)
    # When did the accident occur ?
    date_of_accident = OptionalDateTimeField()

    # Who is declaring the accident ?
    declarant = OptionalForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name="declarant")
    # In what city did the declarant file the claim ?
    declarant_city = OptionalCharField(max_length=40)

    # Who is the victim ?
    victim = OptionalForeignKey(InuitsClaimVictim, on_delete=models.SET_NULL)
    bank_account = OptionalCharField(max_length=30)

    # Where did the accident occur ?
    location = OptionalCharField(max_length=128)
    # What was the scouts group doing when the accident occurred ?
    activity = models.CharField(max_length=1024)
    # During what type of activity did the accident occur ?
    # @TODO serialize to ClaimActivityType
    activity_type = JSONField(max_length=128)
    # What kind of transportation was used when the accident occurred, if any ?
    used_transport = OptionalCharField(max_length=30)
    # Description of the accident
    description = RequiredCharField(max_length=1024)

    damage_type = OptionalCharField(max_length=128)

    # Was there someone else involved in the accident ?
    involved_party_name = OptionalCharField(max_length=1024)
    involved_party_description = OptionalCharField(max_length=1024)
    involved_party_birthdate = OptionalDateField()

    # Was the accident reported by an official instance ?
    official_report_description = OptionalCharField(max_length=1024)
    pv_number = OptionalCharField(max_length=30)

    # Was there a witness to the accident ?
    witness_name = OptionalCharField(max_length=128)
    witness_description = OptionalCharField(max_length=1024)

    # Was someone keeping watch over the scouts group while the accident happened ?
    leadership_description = OptionalCharField(max_length=1024)

    # Administrative personel can add case notes and insurance company case number
    note = OptionalCharField(max_length=1024)
    case_number = OptionalCharField(max_length=30)

    class Meta:
        # Basic permissions for claims are added by ExtendedDjangoModelPermission
        permissions = [
            ("add_insuranceclaim_note", "User can add a note to a claim"),
            ("view_insuranceclaim_note", "Administrative users can view a claim note"),
            ("add_insuranceclaim_case_number", "Users can add a claim case number"),
            ("view_insuranceclaim_case_number", "Administrative users can view a claim case number"),
            ("list_insuranceclaims", "User can view a list of claims"),
            ("view_insuranceclaimattachment_filename", "User can view the filename of a claim attachment"),
        ]

    @property
    def group(self):
        return GroupAdmin().get_group(self.group_group_admin_id)

    def has_attachment(self):
        return hasattr(self, "attachment")
