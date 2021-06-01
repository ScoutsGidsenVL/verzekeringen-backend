from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from ..utils import PostcodeCity
from ..models import InuitsNonMember


def inuits_non_member_create(
    *,
    last_name: str,
    first_name: str,
    phone_number: str,
    birth_date: datetime.date,
    street: str,
    number: str,
    postcode_city: PostcodeCity,
    group_id: str,
    created_by: settings.AUTH_USER_MODEL,
    letter_box: str = "",
    comment: str = "",
) -> InuitsNonMember:
    # validate group
    if group_id not in (group.id for group in created_by.partial_scouts_groups):
        raise ValidationError("Given group %s is not a valid group of user" % group_id)
    non_member = InuitsNonMember(
        last_name=last_name,
        first_name=first_name,
        phone_number=phone_number,
        birth_date=birth_date,
        street=street,
        number=number,
        postcode=int(postcode_city.postcode),
        city=postcode_city.name,
        group_number=group_id,
        letter_box=letter_box,
        comment=comment,
    )
    non_member.full_clean()
    non_member.save()

    return non_member
