from datetime import datetime


class PostcodeCity:
    postcode: str
    name: str

    def __init__(self, postcode, name):
        self.postcode = postcode
        self.name = name


class Address:
    street: str
    number: str
    letter_box: str
    postcode_city: PostcodeCity

    def __init__(self, street, number, postcode_city, letter_box=""):
        self.street = street
        self.number = number
        self.postcode_city = postcode_city
        self.letter_box = letter_box


class GroupAdminMember:
    first_name: str
    last_name: str
    phone_number: str
    birth_date: datetime.date
    email: str
    group_admin_id: str

    membership_number: int
    address: Address

    def __init__(
        self,
        first_name,
        last_name,
        phone_number,
        birth_date,
        email,
        group_admin_id,
        membership_number=None,
        address=None,
    ):
        if not first_name or not last_name or not group_admin_id:
            raise ValueError("first_name, last_name and group_admin_id can not be empty")
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.birth_date = birth_date
        self.email = email
        self.group_admin_id = group_admin_id
        self.membership_number = membership_number
        self.address = address
