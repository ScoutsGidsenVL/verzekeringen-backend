from rest_framework import serializers

from scouts_insurances.locations.models import Country


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ("id", "name")


class BelgianPostalCodeCitySerializer(serializers.Serializer):
    postal_code = serializers.CharField(max_length=4)
    city = serializers.CharField(max_length=40)

    def validate_postal_code(self, value):
        try:
            int_value = int(value)
        except ValueError:
            raise serializers.ValidationError("A Belgian postal code needs to be all numbers, not {}".format(value))
        if int_value < 1000 or int_value > 9999:
            raise serializers.ValidationError(
                "Belgian postal codes are in the range 1000-9999, not {}".format(int_value)
            )

        return value
