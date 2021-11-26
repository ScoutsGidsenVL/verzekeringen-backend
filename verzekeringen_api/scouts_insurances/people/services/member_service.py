from datetime import datetime

from django.conf import settings

from apps.people.models import InuitsNonMemberTemplate, InuitsNonMember

from scouts_insurances.people.models import Member, NonMember


class MemberService:
    def member_create_from_user(
        self,
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
        self,
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
        self,
        *,
        last_name: str,
        first_name: str,
        phone_number: str,
        birth_date: datetime.date = None,
        street: str,
        number: str,
        postal_code: int = None,
        city: str = None,
        letter_box: str = "",
        comment: str = None,
        inuits_non_member_id: str = None,
    ) -> NonMember:
        non_member = NonMember(
            last_name=last_name,
            first_name=first_name,
            phone_number=phone_number,
            birth_date=birth_date,
            street=street,
            number=number,
            postal_code=postal_code,
            city=city,
            letter_box=letter_box,
            comment=comment,
        )
        non_member.full_clean()
        non_member.save()

        if inuits_non_member_id:
            inuits_non_member = InuitsNonMember.objects.filter(id=inuits_non_member_id).first()
            if inuits_non_member:
                InuitsNonMemberTemplate(non_member=non_member, inuits_non_member=inuits_non_member).save()

        return non_member
