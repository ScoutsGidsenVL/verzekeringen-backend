import logging

from django.db import models

from apps.people.models import InuitsAbstractPerson
from apps.people.managers import InuitsNonMemberManager

from scouts_insurances.locations.models import Address

from inuits.models import GenderHelper


logger = logging.getLogger(__name__)


class InuitsNonMember(InuitsAbstractPerson):
    """
    Extra non member class we can use to save unique non members so
    we can have an easy and clean table to search in.
    These are not linked to any insurance but just used to offer some extra
    functionalities that old database doesnt allow us to do.
    """

    objects = InuitsNonMemberManager()

    class Meta:
        pass

    @property
    def full_name(self):
        return self.first_name + " " + self.last_name

    @property
    def get_gender(self):
        gender = GenderHelper.parse_gender(self.gender)

        return gender
