import logging

from rest_framework import serializers

from scouts_auth.inuits.serializers import EnumSerializer
from scouts_insurances.equipment.serializers import TemporaryVehicleInsuranceVehicleSerializer
from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.models.enums import (
    TemporaryVehicleInsuranceCoverageOption,
    TemporaryVehicleInsuranceOption,
)
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import (
    TemporaryVehicleInsuranceCoverageOptionSerializerField,
    TemporaryVehicleInsuranceOptionSerializerField,
)
from scouts_insurances.insurances.utils import InsuranceSettingsHelper
from scouts_insurances.people.serializers import NonMemberSerializer

logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceSerializer(BaseInsuranceSerializer):
    vehicle = TemporaryVehicleInsuranceVehicleSerializer()
    owner = NonMemberSerializer()
    drivers = NonMemberSerializer(many=True)
    insurance_options = TemporaryVehicleInsuranceOptionSerializerField()
    max_coverage = TemporaryVehicleInsuranceCoverageOptionSerializerField(required=False)

    class Meta:
        model = TemporaryVehicleInsurance
        fields = BaseInsuranceFields + ["insurance_options", "max_coverage", "vehicle", "owner", "drivers"]

    def to_internal_value(self, data: dict) -> dict:
        company = data.get("owner", {}).get("company_name", None)
        if company:
            data["owner"]["first_name"] = InsuranceSettingsHelper.get_company_identifier()
            data["owner"]["last_name"] = company

        data = super().to_internal_value(data)

        return data

    def to_representation(self, obj: TemporaryVehicleInsurance) -> dict:
        data = super().to_representation(obj)

        if obj.max_coverage:
            max_coverage = TemporaryVehicleInsuranceCoverageOption.from_choice(obj.max_coverage)
            data["max_coverage"] = EnumSerializer((max_coverage[0], max_coverage[1])).data

        return data

    # def get_insurance_options(self, obj):
    #     logger.debug("OBJ: %s", obj)

    #     return "".join(str(option) for option in obj.insurance_options)

    # @swagger_serializer_method(serializer_or_field=NonMemberSerializer)
    # def get_owner(self, obj):
    #     # @TODO what's this ?
    #     # if obj.owner.first_name == settings.COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME.trim():
    #     #     return NonMemberSerializer(obj.owner).data
    #     # return NonMemberSerializer(obj.owner).data
    #     logger.debug("OWNER DATA: %s", obj)
    #     return NonMemberSerializer(obj.owner).data

    # @swagger_serializer_method(serializer_or_field=EnumSerializer)
    # def get_insurance_options(self, obj):
    #     logger.debug("OBJ: %s", obj)
    #     return EnumSerializer(
    #         [parse_choice_to_tuple(TemporaryVehicleInsuranceOptionApi(option)) for option in obj.insurance_options],
    #         many=True,
    #     ).data

    # @swagger_serializer_method(serializer_or_field=EnumSerializer)
    # def get_max_coverage(self, obj):
    #     if not obj.max_coverage:
    #         return None
    #     return EnumSerializer(parse_choice_to_tuple(TemporaryVehicleInsuranceCoverageOption(obj.max_coverage))).data

    # @swagger_serializer_method(serializer_or_field=InuitsVehicleSerializer)
    # def get_vehicle(self, obj):
    #     vehicle = InuitsVehicle.objects.get(chassis_number=obj.vehicle.chassis_number)

    #     return InuitsVehicleSerializer(vehicle).data

    def validate_insurance_options(self, value: TemporaryVehicleInsuranceOption):
        if not value or value not in TemporaryVehicleInsuranceOption.values:
            raise serializers.ValidationError(
                "At least one insurance option must be selected (invalid value: %s)", value
            )
        return value

    def validate_drivers(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one driver is required")
        return value

    def validate(self, data):
        # Flattened to int at this point
        insurance_option = data.get("insurance_options", [])
        insurance_options = list(str(insurance_option))
        max_coverage = data.get("max_coverage", None)

        if TemporaryVehicleInsuranceOption.COVER_OMNIUM in insurance_options and not max_coverage:
            raise serializers.ValidationError(
                "If 'reeds afgesloten omnium afdekken' is chosen max_coverage is required"
            )
        # @TODO logische fout in frontend ?
        # elif TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM not in insurance_options and max_coverage:
        #     raise serializers.ValidationError(
        #         "If 'reeds afgesloten omnium afdekken' is not chosen max_coverage is not allowed to be given"
        #     )

        if (
            TemporaryVehicleInsuranceOption.COVER_OMNIUM in insurance_options
            and TemporaryVehicleInsuranceOption.OMNIUM in insurance_options
        ):
            raise serializers.ValidationError("'reeds afgesloten omnium afdekken' and 'omnium' are mutually exclusive")
        return data
