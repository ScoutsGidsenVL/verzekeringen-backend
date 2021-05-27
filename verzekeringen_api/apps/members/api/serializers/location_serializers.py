from rest_framework import serializers
from ...services import LocationService
from ...utils import PostcodeCity

# Output
class BelgianPostcodeCityOutputSerializer(serializers.Serializer):
    postcode = serializers.CharField(read_only=True)
    city = serializers.CharField(source="name", read_only=True)


# Input
class BelgianPostcodeCityInputSerializer(serializers.Serializer):
    postcode = serializers.CharField(max_length=4)
    city = serializers.CharField(source="name", max_length=40)

    def validate_postcode(self, value):
        try:
            int_value = int(value)
        except ValueError:
            raise serializers.ValidationError("A postcode needs to be all numbers")
        if int_value < 1000 or int_value > 9999:
            raise serializers.ValidationError("Not a valid postcode")

        return value

    def validate(self, data):
        """
        Validate if postcode and city match, we only do this on input because we want to keep flexibility in system
        """
        if not LocationService.validate_belgian_postcode_city(
            postcode=data.get("postcode"), city_name=data.get("name")
        ):
            raise serializers.ValidationError("Postcode and city do not match")
        return PostcodeCity(postcode=data.get("postcode"), name=data.get("name"))
