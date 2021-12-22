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

    comment = OptionalCharField(max_length=500)
    company_name = OptionalCharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    def __str__(self):
        return "id({}), {}, comment({})".format(self.id, self.person_to_str(), self.comment)
