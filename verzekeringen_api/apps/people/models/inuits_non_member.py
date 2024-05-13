import logging

from apps.people.managers import InuitsNonMemberManager
from scouts_auth.inuits.models import InuitsPerson
from scouts_auth.inuits.models.fields import OptionalCharField

logger = logging.getLogger(__name__)


class InuitsNonMember(InuitsPerson):
    """
    Extra non member class we can use to save unique non members so
    we can have an easy and clean table to search in.
    These are not linked to any insurance but just used to offer some extra
    functionalities that old database doesnt allow us to do.
    """

    objects = InuitsNonMemberManager()

    # FIELDS INHERITED FROM InuitsPersonalDetails
    # first_name    max_length=15           required
    # last_name     max_length=25           required
    # phone_number  max_length=24           optional
    # cell_number   max_length=24           optional
    # email         EmailField              optional
    # birth_date    date                    optional
    # gender        choices=Gender.choices  optional

    # FIELDS INHERITED FROM InuitsAddress
    # street        max_length=100          optional
    # number        max_length=5            optional
    # letter_box    max_length=5            optional
    # postal_code   number                  optional
    # city          max_length=40           optional

    # If set, this denotes a member that will be linked to an insurance that
    # links all people as NonMember
    group_admin_id = OptionalCharField()
    comment = OptionalCharField(max_length=500)
    company_name = OptionalCharField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     self.first_name = kwargs.get("first_name", "")
    #     self.last_name = kwargs.get("last_name", "")
    #     self.

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def has_id(self) -> bool:
        return self.id is not None

    def has_group_admin_id(self) -> bool:
        return self.group_admin_id is not None and len(self.group_admin_id.strip()) > 0

    def is_member(self) -> bool:
        return self.has_group_admin_id()

    def equals(self, instance) -> bool:
        logger.debug(type(instance).__name__)
        logger.debug(self)
        logger.debug(instance)
        return (
            instance is not None
            and type(instance).__name__ == "InuitsNonMember"
            and self.first_name == instance.first_name
            and self.last_name == instance.last_name
            and self.phone_number == instance.phone_number
            and self.cell_number == instance.cell_number
            and self.email == instance.email
            and self.birth_date == instance.birth_date
            and self.gender == instance.gender
            and self.street == instance.street
            and self.number == instance.number
            and self.letter_box == instance.letter_box
            and self.postal_code == instance.postal_code
            and self.city == instance.city
            and self.comment == instance.comment
            and self.group_admin_id == instance.group_admin_id
            and self.company_name == instance.company_name
        )

    def __str__(self):
        return "id({}), {}, comment({})".format(self.id, self.person_to_str(), self.comment)
