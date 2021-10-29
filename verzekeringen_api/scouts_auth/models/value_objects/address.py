from scouts_auth.models.value_objects import PostcodeCity


class GroupAdminAddress:

    id: str
    street: str
    number: str
    letter_box: str
    postcode_city: PostcodeCity
    postal_code: str
    city: str
    country: str
    phone: str
    postal_address: bool
    status: str
    position: dict
    giscode: str
    description: str

    def __init__(
        self,
        id: str = None,
        street: str = None,
        number: str = None,
        letter_box: str = None,
        postcode_city: str = None,
        postal_code: str = None,
        city: str = None,
        country: str = None,
        phone: str = None,
        postal_address: bool = None,
        status: str = None,
        position: dict = None,
        giscode: str = None,
        description: str = None,
    ):
        self.id = id if id else ""
        self.street = street if street else ""
        self.number = number if number else ""
        self.letter_box = letter_box if letter_box else ""
        self.postcode_city = postcode_city
        self.postal_code = postal_code if postal_code else ""
        self.city = city if city else ""
        self.country = country if country else ""
        self.phone = phone if phone else ""
        self.postal_address = postal_address if postal_address else False
        self.status = status if status else ""
        self.position = position if position else {}
        self.giscode = giscode if giscode else ""
        self.description = description if description else ""
