import logging

from rest_framework import serializers

from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.locations.models import Country
from scouts_insurances.locations.serializers import CountrySerializer

from scouts_insurances.equipment.serializers import EquipmentSerializer
from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer

logger = logging.getLogger(__name__)


class EquipmentInsuranceSerializer(BaseInsuranceSerializer):
    equipment = EquipmentSerializer(many=True)
    country = serializers.PrimaryKeyRelatedField(
        queryset=Country.objects.by_insurance_type_id(InsuranceTypeEnum.EQUIPMENT),
        required=False,
    )

    class Meta:
        model = EquipmentInsurance
        fields = BaseInsuranceFields + ["nature", "_country", "postal_code", "city", "equipment"]

    def validate_equipment(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one equipment is required")
        return value

    def validate(self, data):
        postal_code = data.get("postal_code", None)
        city = data.get("city", None)
        country = data.get("_country", None)

        if not (postal_code and city) and not country:
            raise serializers.ValidationError("Either postal code/city or country is required")
        elif (postal_code and city) and country:
            raise serializers.ValidationError("Country and postal_code/city are mutually exclusive fields")
        return data

    def to_representation(self, obj: EquipmentInsurance) -> dict:
        data = super().to_representation(obj)

        data["country"] = data.pop("_country")

        return data
