from scouts_auth.inuits.models.fields import OptionalCharField, OptionalIntegerField


class AbstractScoutsGrouping:

    name = OptionalCharField()
    index = OptionalIntegerField()

    def __init__(self, name: str = "", index: int = -1):
        self.name = name
        self.index = index

    def __str__(self):
        return "name({}), index({})".format(self.name, self.index)
