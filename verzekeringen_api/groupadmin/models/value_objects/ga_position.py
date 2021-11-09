class ScoutsGeoCoordinate:

    imaginary: float
    real: float

    def __init__(self, imaginary: float = 0.0, real: float = 0.0):
        self.imaginary = imaginary
        self.real = real

    def __str__(self):
        return "imaginary({}), real({})".format(self.imaginary, self.real)


class ScoutsPosition:

    latitude: ScoutsGeoCoordinate
    longitude: ScoutsGeoCoordinate

    def __init__(self, latitude: ScoutsGeoCoordinate = None, longitude: ScoutsGeoCoordinate = None):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "latitude({}), longitude({})".format(str(self.latitude), str(self.longitude))
