import logging

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from apps.people.models import InuitsNonMember, InuitsNonMemberTemplate
from scouts_insurances.people.models import NonMember
from scouts_insurances.people.services import NonMemberService

logger = logging.getLogger(__name__)


class InuitsNonMemberService(NonMemberService):
    def inuits_non_member_create(
        self, *, inuits_non_member: InuitsNonMember, created_by: settings.AUTH_USER_MODEL
    ) -> InuitsNonMember:
        # Check if the instance already exists
        if inuits_non_member.has_id():
            logger.debug("Querying for InuitsNonMember with id %s", inuits_non_member.id)
            try:
                object = InuitsNonMember.objects.get(pk=inuits_non_member.id)
                if object:
                    logger.debug("Found InuitsNonMember with id %s, not creating", inuits_non_member.id)
                    return inuits_non_member
                    # return self.inuits_non_member_update(
                    #     inuits_non_member=inuits_non_member, updated_inuits_non_member=object, updated_by=created_by
                    # )
            except ObjectDoesNotExist:
                pass

        logger.debug(
            "Creating InuitsNonMember with name %s %s", inuits_non_member.first_name, inuits_non_member.last_name
        )
        inuits_non_member = InuitsNonMember(
            first_name=inuits_non_member.first_name,
            last_name=inuits_non_member.last_name,
            phone_number=inuits_non_member.phone_number,
            cell_number=inuits_non_member.cell_number,
            birth_date=inuits_non_member.birth_date,
            gender=inuits_non_member.gender,
            street=inuits_non_member.street,
            number=inuits_non_member.number,
            letter_box=inuits_non_member.letter_box,
            postal_code=inuits_non_member.postal_code,
            city=inuits_non_member.city,
            comment=inuits_non_member.comment,
            group_admin_id=inuits_non_member.group_admin_id,
            created_by=created_by,
        )
        inuits_non_member.full_clean()
        inuits_non_member.save()

        return inuits_non_member

    def linked_non_member_create(
        self, inuits_non_member: InuitsNonMember, created_by: settings.AUTH_USER_MODEL
    ) -> NonMember:
        """
        Creates a NonMember

        If the inuits_non_member argument is not a scouts member, then an InuitsNonMember
        will be created and it will be linked to the NonMember.
        """
        if not inuits_non_member.is_member():
            logger.debug("Creating a NonMember and linking it to an InuitsNonMember")

            inuits_non_member = self.inuits_non_member_create(
                inuits_non_member=inuits_non_member, created_by=created_by
            )

            non_member = self.non_member_create(inuits_non_member=inuits_non_member)

            # Can't do the following, because the insurance tables require every non_member to be unique.
            # This means creating a NonMember instance always.
            #
            # non_member_template = InuitsNonMemberTemplate.objects.filter(inuits_non_member=inuits_non_member).last()
            # if non_member_template:
            #     logger.debug("Returning already existing NonMember (id: %s)", non_member_template.non_member.id)
            #     return non_member_template.non_member

            logger.debug("Link NonMember(%s) to InuitsNonMember(%s)", non_member.id, inuits_non_member.id)
            non_member_template = InuitsNonMemberTemplate()
            non_member_template.non_member = non_member
            non_member_template.inuits_non_member = inuits_non_member
            non_member_template.full_clean()
            non_member_template.save()

            return non_member

        return self.non_member_create(inuits_non_member=inuits_non_member)

    def non_member_create(self, inuits_non_member: InuitsNonMember) -> NonMember:
        """
        Creates a NonMember instance.
        """

        non_member = super().non_member_create(
            inuits_id=inuits_non_member.id,
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

        return non_member

    def inuits_non_member_update(
        self,
        *,
        inuits_non_member: InuitsNonMember,
        updated_inuits_non_member: InuitsNonMember,
        updated_by: settings.AUTH_USER_MODEL,
    ) -> InuitsNonMember:
        if inuits_non_member.equals(updated_inuits_non_member):
            return updated_inuits_non_member

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
        inuits_non_member.updated_by = updated_by

        inuits_non_member.full_clean()
        inuits_non_member.save()

        # Check to see if the scouts NonMember instance can also be updated
        non_members = InuitsNonMemberTemplate.objects.all().filter(
            inuits_non_member=inuits_non_member, non_member__in=list(NonMember.objects.all().editable(user=None))
        )
        logger.debug("NON_MEMBERs: %s", non_members)

        for non_member in non_members:
            self.non_member_update(
                non_member=non_member,
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
