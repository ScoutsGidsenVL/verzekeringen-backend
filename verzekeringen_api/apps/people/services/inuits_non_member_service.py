from datetime import datetime


from apps.people.models import InuitsNonMember

from scouts_auth.inuits.models import (
    Gender,
    InuitsPersonalDetails,
    InuitsAddress,
    InuitsCountry,
)
from scouts_auth.inuits.services import InuitsPersonService


class InuitsNonMemberService:
    person_service = InuitsPersonService()

    def inuits_non_member_create(
        self,
        *,
        first_name: str = "",
        last_name: str = "",
        phone_number: str = "",
        cell_number: str = "",
        birth_date: datetime.date = None,
        gender: Gender = Gender.UNKNOWN,
        street: str = "",
        number: str = "",
        letter_box: str = "",
        postal_code: int = None,
        city: str = "",
        country: InuitsCountry = None,
        # group_group_admin_id: str,
        # created_by: settings.AUTH_USER_MODEL = None,
        comment: str = "",
    ) -> InuitsNonMember:
        non_member = InuitsNonMember(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            cell_number=cell_number,
            birth_date=birth_date,
            gender=gender,
            street=street,
            number=number,
            letter_box=letter_box,
            postal_code=postal_code,
            city=city,
            comment=comment,
        )
        non_member.full_clean()
        non_member.save()

        return non_member

    def inuits_non_member_update(self, *, non_member: InuitsNonMember, **fields) -> InuitsNonMember:
        non_member.first_name = fields.get("first_name", non_member.first_name)
        non_member.last_name = fields.get("last_name", non_member.last_name)
        non_member.phone_number = fields.get("phone_number", non_member.phone_number)
        non_member.birth_date = fields.get("birth_date", non_member.birth_date)
        non_member.street = fields.get("street", non_member.street)
        non_member.number = fields.get("number", non_member.number)
        non_member.letter_box = fields.get("letter_box", non_member.letter_box)
        non_member.postal_code = fields.get("postal_code", non_member.postal_code)
        non_member.city = fields.get("city", non_member.city)
        non_member.comment = fields.get("comment", non_member.comment)

        non_member.full_clean()
        non_member.save()

        return non_member
