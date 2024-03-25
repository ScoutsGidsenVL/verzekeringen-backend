from rest_framework import serializers

from scouts_insurances.insurances.models import TemporaryInsurance
from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.locations.models import Country
from scouts_insurances.people.serializers import NonMemberSerializer


class TemporaryInsuranceSerializer(BaseInsuranceSerializer):
    nature = serializers.CharField(max_length=500)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.by_insurance_type_id(InsuranceTypeEnum.TEMPORARY), required=False
    )
    non_members = NonMemberSerializer(many=True)

    class Meta:
        model = TemporaryInsurance
        fields = BaseInsuranceFields + ["nature", "country", "non_members", "postal_code", "city"]

    def validate_non_members(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one non member is required")
        return value

    def validate(self, data: dict) -> dict:
        postal_code = data.get("postal_code", None)
        city = data.get("city", None)
        country = data.get("country", None)

        if not (postal_code and city) and not country:
            raise serializers.ValidationError("Either postal code/city or country is required")
        elif (postal_code and city) and country:
            raise serializers.ValidationError("Country and postal_code/city are mutually exclusive fields")
        return data
