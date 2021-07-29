from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import transaction
from django.conf import settings
from ..models.insurance_claim import InsuranceClaim
from ...members.models import InuitsNonMember


@transaction.atomic
def insurance_claim_create(
    *,
        created_by: settings.AUTH_USER_MODEL,
        id: int = None,
        declarant_city: str = None,
        group_id: str,
        victim_member: str = None,
        victim_non_member: InuitsNonMember = None,
        legal_representative: str = None,
        bank_account: str = None,
        date_of_accident: datetime,
        activity: str = None,
        activity_type: str = None,
        location: str = None,
        used_transport: str = None,
        damage_type: str = None,
        description: str = None,
        involved_party_description: str = None,
        involved_party_birthdate: str = None,
        official_report_description:  str = None,
        pv_number:  str = None,
        witness_name: str = None,
        witness_description:  str = None,
        leadership_description:  str = None
) -> InsuranceClaim:

    # validate group
    if group_id not in (group.id for group in created_by.partial_scouts_groups):
        raise ValidationError("Given group %s is not a valid group of user" % group_id)

    claim = InsuranceClaim(
        date=datetime.now(),
        declarant=created_by,
        declarant_city=declarant_city,
        legal_representative=legal_representative,
        group_number=group_id,
        victim_member_group_admin_id=victim_member,
        victim_non_member=victim_non_member,
        bank_account=bank_account,
        date_of_accident=date_of_accident,
        activity=activity,
        activity_type=activity_type,
        location=location,
        used_transport=used_transport,
        damage_type=damage_type,
        description=description,
        involved_party_description=involved_party_description,
        involved_party_birthdate=involved_party_birthdate,
        official_report_description=official_report_description,
        pv_number=pv_number,
        witness_name=witness_name,
        witness_description=witness_description,
        leadership_description=leadership_description
        )

    claim.full_clean()
    claim.save()

    return claim
