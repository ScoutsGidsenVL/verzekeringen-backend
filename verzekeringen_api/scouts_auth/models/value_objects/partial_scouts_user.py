from datetime import date

from scouts_auth.models.value_objects import GroupAdminLink


class PartialScoutsUser:

    link: GroupAdminLink = None
    first_name: str = None
    last_name: str = None
    birth_date: date = None

    def __init__(
        self, link: GroupAdminLink = None, first_name: str = None, last_name: str = None, birth_date: date = None
    ):
        self.link = link
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date

    def __str__(self):
        return "link({}), first_name({}), last_name({}), birth_date({})".format(
            self.link, self.first_name, self.last_name, self.birth_date
        )
