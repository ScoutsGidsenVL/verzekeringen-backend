from datetime import datetime
from django.conf import settings
from ..models import Member


def member_create_from_user(
    *,
    user: settings.AUTH_USER_MODEL,
    phone_number: str,
) -> Member:
    member = Member(
        last_name=user.last_name,
        first_name=user.first_name,
        phone_number=phone_number,
        email=user.email,
        birth_date=user.birth_date,
        membership_number=user.membership_number,
        group_admin_id=user.group_admin_id,
    )
    member.full_clean()
    member.save()

    return member
