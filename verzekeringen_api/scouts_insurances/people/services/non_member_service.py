from datetime import datetime

from scouts_insurances.people.models import NonMember


class NonMemberService:
    def non_member_create(
        self,
        *,
        first_name: str,
        last_name: str,
        phone_number: str = None,
        birth_date: datetime.date = None,
        street: str = None,
        number: str = None,
        letter_box: str = None,
        postal_code: int = None,
        city: str = None,
        comment: str = None,
    ) -> NonMember:
        non_member = NonMember(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            birth_date=birth_date,
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

    def non_member_update(
        self,
        *,
        non_member: NonMember,
        first_name: str,
        last_name: str,
        phone_number: str = None,
        birth_date: datetime.date = None,
        street: str = None,
        number: str = None,
        letter_box: str = None,
        postal_code: int = None,
        city: str = None,
        comment: str = None,
    ) -> NonMember:
        non_member.first_name = first_name
        non_member.last_name = last_name
        non_member.phone_number = phone_number
        non_member.birth_date = birth_date
        non_member.street = street
        non_member.number = number
        non_member.letter_box = letter_box
        non_member.postal_code = postal_code
        non_member.city = city
        non_member.comment = comment

        non_member.full_clean()
        non_member.save()

        return non_member
