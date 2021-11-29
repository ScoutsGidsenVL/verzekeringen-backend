from rest_framework import serializers

from scouts_insurances.locations.models import Country

from scouts_insurances.people.serializers import NonMemberSerializer
from scouts_insurances.insurances.models import TemporaryInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer


class TemporaryInsuranceSerializer(BaseInsuranceSerializer):
    nature = serializers.CharField(max_length=500)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.by_type(2), required=False)
    non_members = NonMemberSerializer(many=True)

    class Meta:
        model = TemporaryInsurance
        fields = BaseInsuranceFields + ("nature", "country", "postal_code", "city", "non_members")

    def validate_non_members(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one non member is required")
        return value

    def validate(self, data):
        postal_code = data.get("postal_code", None)
        city = data.get("city", None)
        country = data.get("country", None)
        if not (postal_code and city) and not country:
            raise serializers.ValidationError("Either postal code/city or country is required")
        elif (postal_code and city) and country:
            raise serializers.ValidationError("Country and postal_code/city are mutually exclusive fields")
        return data
