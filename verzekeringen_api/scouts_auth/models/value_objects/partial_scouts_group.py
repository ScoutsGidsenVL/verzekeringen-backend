class PartialScoutsGroup:
    """
    An group reference contained in the response from an API call,
    used to fully load a Group when needed.
    """

    id: str
    href: str

    def __init__(self, identifier: str, href: str):
        self.id = identifier
        self.href = href
