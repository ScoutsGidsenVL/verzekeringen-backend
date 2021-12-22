from django.core.exceptions import ValidationError

from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.models.fields import OptionalCharField


class InuitsClaimVictim(InuitsPerson):

    legal_representative = OptionalCharField(max_length=128)
    group_admin_id = OptionalCharField(max_length=64)
    membership_number = OptionalCharField(max_length=64)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.non_member and self.group_admin_id:
            raise ValidationError("Victim cannot be member and non member at same time")
