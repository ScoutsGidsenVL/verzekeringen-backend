import logging

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from jsonfield import JSONField

from apps.insurances.managers import InsuranceClaimManager

from apps.members.models import InuitsNonMember

from groupadmin.models import ScoutsUser, ScoutsMember, PostcodeCity, ScoutsAddress
from groupadmin.services import GroupAdmin

from inuits.models import Gender


logger = logging.getLogger(__name__)


class InsuranceClaimVictim(models.Model):
    id = models.AutoField(primary_key=True)
    last_name = models.CharField(max_length=25)
    first_name = models.CharField(max_length=15)
    birth_date = models.DateField(null=True, blank=True)
    street = models.CharField(max_length=100)
    number = models.CharField(max_length=5)
    letter_box = models.CharField(max_length=5, blank=True)
    # Making postcode int field is bad practice but keeping it because of compatibility with actual NonMember
    postcode = models.IntegerField()
    city = models.CharField(max_length=40)
    email = models.EmailField(max_length=60, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, choices=Gender.choices, default=Gender.UNKNOWN)
    legal_representative = models.CharField(max_length=128, null=True, blank=True)

    group_admin_id = models.CharField(db_column="ga_id", max_length=255, blank=True, null=True)
    #
    non_member = models.ForeignKey(
        InuitsNonMember,
        null=True,
        related_name="claim_victim",
        blank=True,
        on_delete=models.SET_NULL,
    )

    _member_detail: ScoutsMember = None

    def get_member_number(self, active_user: settings.AUTH_USER_MODEL):
        if self.group_admin_id:
            if not self._member_detail:
                self._member_detail = GroupAdmin().group_admin_member_detail(
                    active_user=active_user, group_admin_id=str(self.group_admin_id)
                )
            return self._member_detail.membership_number
        return None

    @property
    def postcode_city(self):
        return PostcodeCity(postcode=self.postcode, name=self.city)

    @property
    def address(self):
        return ScoutsAddress(
            street=self.street, number=self.number, letter_box=self.letter_box, postcode_city=self.postcode_city
        )

    def get_gender(self):
        return self.gender

    def clean(self):
        if self.non_member and self.group_admin_id:
            raise ValidationError("Victim cannot be member and non member at same time")


class InsuranceClaim(models.Model):
    group_group_admin_id = models.CharField(max_length=6, null=True)
    date = models.DateTimeField(blank=True)
    declarant = models.ForeignKey(ScoutsUser, on_delete=models.SET_NULL, null=True, blank=False)
    declarant_city = models.CharField(max_length=30, null=True, blank=True)
    victim = models.ForeignKey(InsuranceClaimVictim, on_delete=models.SET_NULL, null=True, blank=False)
    bank_account = models.CharField(max_length=30, null=True, blank=True)
    date_of_accident = models.DateTimeField()
    activity = models.CharField(max_length=1024)
    # Custom JSONField
    activity_type = JSONField(max_length=128)
    location = models.CharField(max_length=128, null=True, blank=True)
    used_transport = models.CharField(max_length=30, null=True, blank=True)
    damage_type = models.CharField(max_length=128, null=True, blank=True)
    description = models.CharField(max_length=1024)

    involved_party_name = models.CharField(max_length=1024, null=True, blank=True)
    involved_party_description = models.CharField(max_length=1024, null=True, blank=True)
    involved_party_birthdate = models.DateField(null=True, blank=True)

    official_report_description = models.CharField(max_length=1024, null=True, blank=True)
    pv_number = models.CharField(max_length=30, null=True, blank=True)

    witness_name = models.CharField(max_length=128, null=True, blank=True)
    witness_description = models.CharField(max_length=1024, null=True, blank=True)

    leadership_description = models.CharField(max_length=1024, null=True, blank=True)

    note = models.CharField(max_length=1024, null=True, blank=True)
    case_number = models.CharField(max_length=30, null=True, blank=True)

    objects = InsuranceClaimManager()

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
