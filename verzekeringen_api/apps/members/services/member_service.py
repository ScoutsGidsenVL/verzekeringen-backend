from datetime import datetime
from django.conf import settings
from ..utils import PostcodeCity
from ..models import Member, NonMember


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


def member_create(
    *,
    last_name: str,
    first_name: str,
    phone_number: str,
    birth_date: datetime.date,
    email: str,
    membership_number: int,
    group_admin_id: str,
) -> Member:
    member = Member(
        last_name=last_name,
        first_name=first_name,
        phone_number=phone_number,
        email=email,
        birth_date=birth_date,
        membership_number=membership_number,
        group_admin_id=group_admin_id,
    )
    member.full_clean()
    member.save()

    return member


def non_member_create(
    *,
    last_name: str,
    first_name: str,
    phone_number: str,
    birth_date: datetime.date,
    street: str,
    number: str,
    postcode_city: PostcodeCity,
    letter_box: str = "",
    comment: str = "",
) -> NonMember:
    non_member = NonMember(
        last_name=last_name,
        first_name=first_name,
        phone_number=phone_number,
        birth_date=birth_date,
        street=street,
        number=number,
        postcode=int(postcode_city.postcode),
        city=postcode_city.name,
        letter_box=letter_box,
        comment=comment,
    )
    non_member.full_clean()
    non_member.save()

    return non_member
