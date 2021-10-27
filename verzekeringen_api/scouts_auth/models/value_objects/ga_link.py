
class GroupAdminLink:
    """This class captures the data returned by GroupAdmin containing links to the full references info."""

    rel: str = None
    href: str = None
    method: str = None
    sections: list = None

    def __init__(self, rel: str = None, href: str = None, method: str = None, sections: list = None):
        self.rel = rel
        self.href = href
        self.method = href
        self.sections = sections if sections is not None else []
