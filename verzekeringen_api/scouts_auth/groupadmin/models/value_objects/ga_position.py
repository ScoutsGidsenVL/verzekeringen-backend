from django.db import models


class AbstractScoutsGeoCoordinate:

    imaginary = models.FloatField()
    real = models.FloatField()

    def __init__(self, imaginary: float = 0.0, real: float = 0.0):
        self.imaginary = imaginary
        self.real = real

    def __str__(self):
        return "imaginary({}), real({})".format(self.imaginary, self.real)


class AbstractScoutsPosition:

    latitude: AbstractScoutsGeoCoordinate = models.JSONField()
    longitude: AbstractScoutsGeoCoordinate = models.JSONField()

    def __init__(self, latitude: AbstractScoutsGeoCoordinate = None, longitude: AbstractScoutsGeoCoordinate = None):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return "latitude({}), longitude({})".format(str(self.latitude), str(self.longitude))
