from django.conf import settings
from django.db import models
from django.db.models import BooleanField
from jsonfield import JSONField

from apps.insurances.managers import InsuranceClaimManager
from apps.people.models import InuitsClaimVictim
from scouts_auth.groupadmin.models import AbstractScoutsGroup, AbstractScoutsMember
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
    involved_party = OptionalCharField(max_length=30, blank=True, null=True, default=None)
    involved_party_name = OptionalCharField(max_length=1024)
    involved_party_description = OptionalCharField(max_length=1024)
    involved_party_birthdate = OptionalDateField()

    # Was the accident reported by an official instance ?
    official_report = OptionalCharField(max_length=30, blank=True, null=True, default=None)

    official_report_description = OptionalCharField(max_length=1024)
    pv_number = OptionalCharField(max_length=30)

    # Was there a witness to the accident ?
    witness = OptionalCharField(max_length=30, blank=True, null=True, default=None)
    witness_name = OptionalCharField(max_length=128)
    witness_description = OptionalCharField(max_length=1024)

    # Was someone keeping watch over the scouts group while the accident happened ?
    leadership = OptionalCharField(max_length=30, blank=True, null=True, default=None)
    leadership_description = OptionalCharField(max_length=1024)

    # Administrative personel can add case notes and insurance company case number
    note = OptionalCharField(max_length=1024)
    case_number = OptionalCharField(max_length=30)

    attachment_name = OptionalCharField(max_length=1024, blank=True, null=True, default=None)
    # Full scouts group details
    _group: AbstractScoutsGroup = None
    # Full groupadmin member data for the declarant
    _declarant_member: AbstractScoutsMember = None

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
    def group(self) -> AbstractScoutsGroup:
        return self._group

    @group.setter
    def group(self, group: AbstractScoutsGroup):
        self._group = group

    @property
    def declarant_member(self) -> AbstractScoutsMember:
        return self._declarant_member

    @declarant_member.setter
    def declarant_member(self, declarant_member: AbstractScoutsMember):
        self._declarant_member = declarant_member

    def has_involved_party(self):
        return True if self.involved_party == "yes" else False

    def has_official_report(self):
        return True if self.official_report == "yes" else False

    def has_witness(self):
        return True if self.witness == "yes" else False

    def has_leadership(self):
        return True if self.leadership == "yes" else False

    def has_attachment(self):
        return hasattr(self, "attachment")
