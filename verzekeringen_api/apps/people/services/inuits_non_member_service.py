import logging
from datetime import datetime

from django.conf import settings


from apps.people.models import InuitsNonMember, InuitsNonMemberTemplate

from scouts_insurances.people.models import NonMember
from scouts_insurances.people.services import NonMemberService

from scouts_auth.inuits.models import (
    Gender,
    InuitsCountry,
)


logger = logging.getLogger(__name__)


class InuitsNonMemberService(NonMemberService):
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

    def non_member_create(self, inuits_non_member: InuitsNonMember) -> NonMember:
        """
        Creates a NonMember instance.
        """

        # Can't do the following, because the insurance tables require every non_member to be unique.
        # This means creating a NonMember instance always.
        #
        # non_member_template = InuitsNonMemberTemplate.objects.filter(inuits_non_member=inuits_non_member).last()
        # if non_member_template:
        #     logger.debug("Returning already existing NonMember (id: %s)", non_member_template.non_member.id)
        #     return non_member_template.non_member

        non_member = super().non_member_create(
            first_name=inuits_non_member.first_name,
            last_name=inuits_non_member.last_name,
            phone_number=inuits_non_member.phone_number,
            birth_date=inuits_non_member.birth_date,
            street=inuits_non_member.street,
            number=inuits_non_member.number,
            letter_box=inuits_non_member.letter_box,
            postal_code=inuits_non_member.postal_code,
            city=inuits_non_member.city,
            comment=inuits_non_member.comment,
        )

        non_member_template = InuitsNonMemberTemplate()
        non_member_template.non_member = non_member
        non_member_template.inuits_non_member = inuits_non_member
        non_member_template.full_clean()
        non_member_template.save()

        return non_member

    def inuits_non_member_update(
        self, *, inuits_non_member: InuitsNonMember, updated_inuits_non_member: InuitsNonMember
    ) -> InuitsNonMember:
        # Update the InuitsNonMember instance
        inuits_non_member.first_name = (
            updated_inuits_non_member.first_name
            if updated_inuits_non_member.first_name
            else inuits_non_member.first_name
        )
        inuits_non_member.last_name = (
            updated_inuits_non_member.last_name if updated_inuits_non_member.last_name else inuits_non_member.last_name
        )
        inuits_non_member.phone_number = (
            updated_inuits_non_member.phone_number
            if updated_inuits_non_member.phone_number
            else inuits_non_member.phone_number
        )
        inuits_non_member.birth_date = (
            updated_inuits_non_member.birth_date
            if updated_inuits_non_member.birth_date
            else inuits_non_member.birth_date
        )
        inuits_non_member.street = (
            updated_inuits_non_member.street if updated_inuits_non_member.street else inuits_non_member.street
        )
        inuits_non_member.number = (
            updated_inuits_non_member.number if updated_inuits_non_member.number else inuits_non_member.number
        )
        inuits_non_member.letter_box = (
            updated_inuits_non_member.letter_box
            if updated_inuits_non_member.letter_box
            else inuits_non_member.letter_box
        )
        inuits_non_member.postal_code = (
            updated_inuits_non_member.postal_code
            if updated_inuits_non_member.postal_code
            else inuits_non_member.postal_code
        )
        inuits_non_member.city = (
            updated_inuits_non_member.city if updated_inuits_non_member.city else inuits_non_member.city
        )
        inuits_non_member.comment = (
            updated_inuits_non_member.comment if updated_inuits_non_member.comment else inuits_non_member.comment
        )

        inuits_non_member.full_clean()
        inuits_non_member.save()

        # Check to see if the scouts NonMember instance can also be updated
        non_members = InuitsNonMemberTemplate.objects.all().filter(
            inuits_non_member=inuits_non_member, non_member__in=list(NonMember.objects.all().editable(user=None))
        )
        logger.debug("NON_MEMBERs: %s", non_members)

        return inuits_non_member

    def check_editable_templates(self, user: settings.AUTH_USER_MODEL):
        non_editable_non_members = NonMember.objects.all().non_editable(user=user)
        logger.debug("NON EDITABLE NON MEMBERS: %s", non_editable_non_members)

        non_editable_templates = InuitsNonMemberTemplate.objects.all().filter(non_member__in=non_editable_non_members)
        logger.debug("NON EDITABLE TEMPLATES: %s", non_editable_templates)

        for non_editable_template in non_editable_templates:
            non_editable_template.editable = False
            non_editable_template.full_clean()
            non_editable_template.save()

        logger.debug("EDITABLE: %s", NonMember.objects.all().editable(user=user))
        logger.debug("TEMPLATE EDITABLE: %s", NonMember.objects.all().template_editable(user=user))
