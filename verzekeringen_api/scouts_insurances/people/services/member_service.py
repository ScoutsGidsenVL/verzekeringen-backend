import logging
from datetime import datetime

from django.conf import settings

from scouts_insurances.people.models import Member


logger = logging.getLogger(__name__)


class MemberService:
    def member_create_from_user(
        self,
        *,
        user: settings.AUTH_USER_MODEL,
    ) -> Member:
        return self.member_create(
            first_name=user.first_name,
            last_name=user.last_name,
            phone_number=user.phone_number,
            birth_date=user.birth_date,
            email=user.email,
            membership_number=user.membership_number,
            group_admin_id=user.group_admin_id,
        )

    def member_create(
        self,
        *,
        first_name: str,
        last_name: str,
        phone_number: str,
        birth_date: datetime.date,
        email: str,
        membership_number: int,
        group_admin_id: str,
    ) -> Member:
        try:
            member = Member.objects.get(group_admin_id=group_admin_id)

            if member:
                logger.debug("Member with group admin id %s already exists in Member", group_admin_id)
                return member
        except Exception:
            pass

        member = Member(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            birth_date=birth_date,
            membership_number=membership_number,
            group_admin_id=group_admin_id,
        )
        member.full_clean()
        member.save()

        return member
