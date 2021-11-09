import logging

from groupadmin.models import ScoutsGeoCoordinate, ScoutsPosition

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsGeoCoordinateSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {"imaginary": data.pop("imag", None), "real": data.pop("real", None)}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsGeoCoordinate:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsGeoCoordinate:
        if validated_data is None:
            return None

        instance = ScoutsGeoCoordinate()

        instance.imaginary = validated_data.pop("imaginary", None)
        instance.real = validated_data.pop("real", None)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsPositionSerializer(NonModelSerializer):
    def _parse_geo_coordinate(self, geo_coordinate: dict, name: str) -> dict:
        if isinstance(geo_coordinate, dict):
            imaginary = geo_coordinate.pop("imag", None)
            real = geo_coordinate.pop("real", None)

            if imaginary is None and real is None:
                logger.error("GA: returned a %s without imaginary or real part", name)
            else:
                geo_coordinate = {"imag": imaginary, "real": real}
        else:
            geo_coordinate = {"real": geo_coordinate}

        return geo_coordinate

    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        latitude = data.pop("latitude", None)
        longitude = data.pop("longitude", None)

        if latitude is None or longitude is None:
            logger.error("GA: returned a position without latitude and longitude")

        latitude = self._parse_geo_coordinate(latitude, "latitude")
        longitude = self._parse_geo_coordinate(longitude, "longitude")

        validated_data = {
            "latitude": ScoutsGeoCoordinateSerializer().to_internal_value(latitude),
            "longitude": ScoutsGeoCoordinateSerializer().to_internal_value(longitude),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsPosition:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsPosition:
        if validated_data is None:
            return None

        instance = ScoutsPosition()

        instance.latitude = ScoutsGeoCoordinateSerializer().create(validated_data.pop("latitude", None))
        instance.longitude = ScoutsGeoCoordinateSerializer().create(validated_data.pop("longitude", None))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
