import logging

from rest_framework import serializers

from scouts_insurances.people.serializers import NonMemberSerializer
from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.models.enums import (
    TemporaryVehicleInsuranceOptionApi,
)
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer
from scouts_insurances.insurances.serializers.fields import (
    TemporaryVehicleInsuranceOptionSerializerField,
    TemporaryVehicleInsuranceCoverageOptionSerializerField,
)

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class TemporaryVehicleInsuranceSerializer(BaseInsuranceSerializer):
    drivers = NonMemberSerializer(many=True)
    owner = NonMemberSerializer()
    insurance_options = TemporaryVehicleInsuranceOptionSerializerField(many=True)
    # insurance_options = serializers.SerializerMethodField()
    max_coverage = TemporaryVehicleInsuranceCoverageOptionSerializerField()

    class Meta:
        model = TemporaryVehicleInsurance
        fields = BaseInsuranceFields + ["insurance_options", "max_coverage", "owner", "drivers"]

    def get_insurance_options(self, obj):
        logger.debug("OBJ: %s", obj)

        return "".join(str(option) for option in obj.insurance_options)

    def to_internal_value(self, data: dict) -> dict:
        logger.debug("TEMPORARY VEHICLE INSURANCE SERIALIZER TO_INTERNAL_VALUE: %s", data)
        data.pop("responsible_phone_number", None)
        data.pop("group_admin_id", None)
        insurance_options = data.pop("insurance_options", [])
        data = super().to_internal_value(data)
        logger.debug("TEMPORARY VEHICLE INSURANCE SERIALIZER TO_INTERNAL_VALUE: %s", data)
        data["insurance_options"] = insurance_options
        return data
        # data["scouts_group"] = GroupAdmin().get_group(
        #     active_user=self.context.get("request").user, group_group_admin_id=data.pop("group_group_admin_id")
        # )

        # return data

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

    def validate_insurance_options(self, value: list):
        if len(value) == 0:
            raise serializers.ValidationError("At least one insurance option must be selected")
        return value

    def validate_drivers(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one driver is required")
        return value

    def validate(self, data):
        logger.debug("DATA: %s", data)
        insurance_options = data.get("insurance_options", [])
        max_coverage = data.get("max_coverage", None)

        if TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM in insurance_options and not max_coverage:
            raise serializers.ValidationError(
                "If 'reeds afgesloten omnium afdekken' is chosen max_coverage is required"
            )
        # @TODO logische fout in frontend ?
        # elif TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM not in insurance_options and max_coverage:
        #     raise serializers.ValidationError(
        #         "If 'reeds afgesloten omnium afdekken' is not chosen max_coverage is not allowed to be given"
        #     )

        if (
            TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM in insurance_options
            and TemporaryVehicleInsuranceOptionApi.OMNIUM in insurance_options
        ):
            raise serializers.ValidationError("'reeds afgesloten omnium afdekken' and 'omnium' are mutually exclusive")
        return data
