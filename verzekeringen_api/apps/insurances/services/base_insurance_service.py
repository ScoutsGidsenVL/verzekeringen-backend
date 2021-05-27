from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from apps.scouts_auth.utils import Group
from apps.members.models import Member
from apps.members.services import MemberService
from ..models import BaseInsurance, InsuranceType
from ..models.enums import InsuranceStatus


def base_insurance_creation_fields(
    *,
    type: InsuranceType,
    group_id: str,
    start_date: datetime.date,
    end_date: datetime.date,
    responsible_phone_number: str,
    created_by: settings.AUTH_USER_MODEL,
    total_cost: int,
    comment: str = "",
) -> dict:
    # validate group
    created_by.fetch_detailed_group_info()
    group_object = next(
        (scouts_group for scouts_group in created_by.scouts_groups if scouts_group.id == group_id), None
    )
    if not group_object:
        raise ValidationError("Given group %s is not a valid group of user" % group_id)
    member = MemberService.member_create_from_user(user=created_by, phone_number=responsible_phone_number)
    fields = {
        "status": InsuranceStatus.NEW,
        "type": type,
        "group": group_object,
        "start_date": start_date,
        "end_date": end_date,
        "total_cost": total_cost,
        "responsible_member": member,
        "comment": comment,
        "created_on": timezone.now(),
    }

    return fields
