class Group:
    id: str
    name: str
    location: str

    def __init__(self, id, name, location):
        self.id = id
        self.name = name
        self.location = location


class PartialGroup:
    id: str
    href: str

    def __init__(self, id, href):
        self.id = id
        self.href = href
