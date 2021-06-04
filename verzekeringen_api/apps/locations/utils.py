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
