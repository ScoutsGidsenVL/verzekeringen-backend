from django.db import models

from inuits.models import AbstractModel
from inuits.models.fields import OptionalCharField


class GroupAdminLink(AbstractModel):
    """This class captures the data returned by GroupAdmin containing links to the full references info."""

    rel: str = OptionalCharField()
    href: str = OptionalCharField()
    method: str = OptionalCharField()
    sections: list = None

    def __init__(self, rel: str = "", href: str = "", method: str = "", sections: list = None):
        self.rel = rel
        self.href = href
        self.method = method
        self.sections = sections if sections else []

    def __str__(self):
        return "rel({}), href({}), method({}), sections({})".format(
            self.rel,
            self.href,
            self.method,
            ", ".join(str(section) for section in self.sections),
        )
