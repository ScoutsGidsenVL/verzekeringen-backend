from groupadmin.models.value_objects import PostcodeCity, ScoutsPosition


class ScoutsAddress:

    group_admin_id: str
    street: str
    number: str
    letter_box: str
    postcode_city: PostcodeCity
    postal_code: str
    city: str
    country: str
    phone_number: str
    postal_address: bool
    status: str
    position: ScoutsPosition
    giscode: str
    description: str

    def __init__(
        self,
        group_admin_id: str = "",
        street: str = "",
        number: str = "",
        letter_box: str = "",
        postcode_city: str = "",
        postal_code: str = "",
        city: str = "",
        country: str = "",
        phone_number: str = "",
        postal_address: bool = False,
        status: str = "",
        position: ScoutsPosition = None,
        giscode: str = "",
        description: str = "",
    ):
        self.group_admin_id = group_admin_id
        self.street = street
        self.number = number
        self.letter_box = letter_box
        self.postcode_city = postcode_city
        self.postal_code = postal_code
        self.city = city
        self.country = country
        self.phone_number = phone_number
        self.postal_address = postal_address
        self.status = status
        self.position = position
        self.giscode = giscode
        self.description = description

    def __str__(self):
        return "group_admin_id({}), street({}), number({}), letter_box({}), postcode_city({}), postal_code({}), city({}), country({}), phone_number({}), postal_address({}), status({}), position({}), giscode({}), description({})".format(
            self.group_admin_id,
            self.street,
            self.number,
            self.letter_box,
            str(self.postcode_city),
            self.postal_code,
            self.city,
            self.country,
            self.phone_number,
            self.postal_address,
            self.status,
            str(self.position),
            self.giscode,
            self.description,
        )