from scouts_auth.inuits.models.fields import OptionalCharField


class AbstractScoutsValue:

    key = OptionalCharField()
    value = OptionalCharField()

    def __init__(self, key: str = "", value: str = ""):
        self.key = key
        self.value = value

    def __str__(self):
        return "[key({}), value({})]".format(self.key, self.value)
