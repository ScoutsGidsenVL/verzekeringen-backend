from datetime import datetime
from django.conf import settings
from django.core.exceptions import ValidationError
from ..utils import PostcodeCity
from ..models import InuitsNonMember


def inuits_non_member_create(
    *,
    last_name: str,
    first_name: str,
    phone_number: str = None,
    birth_date: datetime.date = None,
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


def inuits_non_member_update(*, non_member: InuitsNonMember, **fields) -> InuitsNonMember:
    non_member.last_name = fields.get("last_name", non_member.last_name)
    non_member.first_name = fields.get("first_name", non_member.first_name)
    non_member.phone_number = fields.get("phone_number", non_member.phone_number)
    non_member.birth_date = fields.get("birth_date", non_member.birth_date)
    non_member.street = fields.get("street", non_member.street)
    non_member.number = fields.get("number", non_member.number)
    non_member.letter_box = fields.get("letter_box", non_member.letter_box)
    non_member.comment = fields.get("comment", non_member.comment)

    if fields.get("postcode_city", None):
        postcode_city = fields.get("postcode_city")
        non_member.postcode = int(postcode_city.postcode)
        non_member.city = postcode_city.name

    non_member.full_clean()
    non_member.save()

    return non_member
