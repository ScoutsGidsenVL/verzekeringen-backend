from django.db import models
from django.core.exceptions import ValidationError

from apps.people.models import InuitsNonMember
from scouts_auth.inuits.models import InuitsPerson


from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsClaimVictim(InuitsPerson):
    id = models.AutoField(primary_key=True)
    legal_representative = OptionalCharField(max_length=128)
    group_admin_id = OptionalCharField(max_length=64)
    membership_number = OptionalCharField(max_length=64)
    #
    non_member = models.ForeignKey(
        InuitsNonMember,
        null=True,
        related_name="claim_victim",
        blank=True,
        on_delete=models.SET_NULL,
    )

    def get_gender(self):
        return self.gender

    def clean(self):
        if self.non_member and self.group_admin_id:
            raise ValidationError("Victim cannot be member and non member at same time")
