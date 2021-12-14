import logging

from apps.people.managers import InuitsNonMemberManager

from scouts_auth.inuits.models import InuitsPerson, GenderHelper
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

    comment = OptionalCharField(max_length=500)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name
