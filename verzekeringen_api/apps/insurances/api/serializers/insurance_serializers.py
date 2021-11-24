import logging

from django.conf import settings
from django.db.models import Q
from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from apps.base.serializers import EnumOutputSerializer, DateTimeTZField
from apps.base.helpers import parse_choice_to_tuple

from apps.equipment.models import InuitsVehicle
from apps.equipment.api.serializers import (
    InuitsVehicleOutputSerializer,
    VehicleOutputSerializer,
    VehicleInputSerializer,
    VehicleWithChassisInputSerializer,
    EquipmentNestedOutputSerializer,
    EquipmentInputSerializer,
)
from apps.members.api.serializers import (
    MemberNestedOutputSerializer,
    NonMemberNestedOutputSerializer,
    NonMemberCompanyNestedOutputSerializer,
    NonMemberCreateInputSerializer,
    NonMemberOrCompanyCreateInputSerializer,
)
from apps.locations.api.serializers import (
    CountryOutputSerializer,
)
from apps.locations.models import Country
from apps.insurances.models import (
    BaseInsurance,
    ActivityInsurance,
    ActivityInsuranceAttachment,
    TemporaryInsurance,
    TravelAssistanceInsurance,
    TemporaryVehicleInsurance,
    EquipmentInsurance,
    EventInsurance,
    EventInsuranceAttachment,
)
from apps.insurances.models.enums import (
    InsuranceStatus,
    GroupSize,
    EventSize,
    TemporaryVehicleInsuranceOptionApi,
    TemporaryVehicleInsuranceCoverageOption,
)
from apps.insurances.api.serializers import (
    InsuranceTypeOutputSerializer,
    EventInsuranceAttachmentSerializer,
    ActivityInsuranceAttachmentSerializer,
)
from groupadmin.serializers import (
    ScoutsGroupSerializer,
    BelgianPostcodeCitySerializer,
)


logger = logging.getLogger(__name__)


class InsuranceCostOutputSerializer(serializers.Serializer):
    total_cost = serializers.DecimalField(max_digits=7, decimal_places=2)


class InsuranceListOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    scouts_group = ScoutsGroupSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)
    start_date = DateTimeTZField()
    end_date = DateTimeTZField()
    created_on = DateTimeTZField()

    class Meta:
        model = BaseInsurance
        fields = ("id", "status", "type", "scouts_group", "start_date", "end_date", "responsible_member", "created_on")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data


# Just some a tuple so we dont need to copy everything (cannot use inheritance because Meta does not get inherited)
base_insurance_detail_fields = (
    "id",
    "status",
    "type",
    "scouts_group",
    "responsible_member",
    "start_date",
    "end_date",
    "comment",
    "vvks_comment",
    "total_cost",
    "created_on",
    "editable",
)


class BaseInsuranceDetailOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    scouts_group = ScoutsGroupSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)
    start_date = DateTimeTZField()
    end_date = DateTimeTZField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    vvks_comment = serializers.CharField(max_length=500, required=False, allow_blank=True)

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data


class BaseInsuranceCreateInputSerializer(serializers.Serializer):
    group_group_admin_id = serializers.CharField(max_length=6)
    start_date = DateTimeTZField()
    end_date = DateTimeTZField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    responsible_phone_number = serializers.CharField(max_length=15, required=False)


class TemporaryInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    postcode_city = BelgianPostcodeCitySerializer()
    non_members = NonMemberNestedOutputSerializer(many=True)
    country = CountryOutputSerializer()

    class Meta:
        model = TemporaryInsurance
        fields = base_insurance_detail_fields + ("nature", "country", "postcode_city", "non_members")


class TemporaryInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.by_type(2), required=False)
    postcode_city = BelgianPostcodeCitySerializer(required=False)
    non_members = NonMemberCreateInputSerializer(many=True)

    def validate_non_members(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one non member is required")
        return value

    def validate(self, data):
        if not data.get("postcode_city") and not data.get("country"):
            raise serializers.ValidationError("Either postcode_city or country is required")
        elif data.get("postcode_city") and data.get("country"):
            raise serializers.ValidationError("Country and postcode_city are mutually exclusive fields")
        return data


class TemporaryVehicleInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    drivers = NonMemberNestedOutputSerializer(many=True)
    owner = serializers.SerializerMethodField()
    # vehicle = VehicleWithChassisOutputSerializer(read_only=True)
    vehicle = serializers.SerializerMethodField()
    insurance_options = serializers.SerializerMethodField()
    max_coverage = serializers.SerializerMethodField()

    class Meta:
        model = TemporaryVehicleInsurance
        fields = base_insurance_detail_fields + ("insurance_options", "max_coverage", "vehicle", "owner", "drivers")

    @swagger_serializer_method(serializer_or_field=NonMemberNestedOutputSerializer)
    def get_owner(self, obj):
        if obj.owner.first_name == settings.COMPANY_NON_MEMBER_DEFAULT_FIRST_NAME:
            return NonMemberCompanyNestedOutputSerializer(obj.owner).data
        return NonMemberNestedOutputSerializer(obj.owner).data

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_insurance_options(self, obj):
        return EnumOutputSerializer(
            [parse_choice_to_tuple(TemporaryVehicleInsuranceOptionApi(option)) for option in obj.insurance_options],
            many=True,
        ).data

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_max_coverage(self, obj):
        if not obj.max_coverage:
            return None
        return EnumOutputSerializer(
            parse_choice_to_tuple(TemporaryVehicleInsuranceCoverageOption(obj.max_coverage))
        ).data

    @swagger_serializer_method(serializer_or_field=InuitsVehicleOutputSerializer)
    def get_vehicle(self, obj):
        vehicle = InuitsVehicle.objects.get(chassis_number=obj.vehicle.chassis_number)

        return InuitsVehicleOutputSerializer(vehicle).data


class TemporaryVehicleInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    insurance_options = serializers.MultipleChoiceField(choices=TemporaryVehicleInsuranceOptionApi.choices)
    max_coverage = serializers.ChoiceField(choices=TemporaryVehicleInsuranceCoverageOption.choices, required=False)
    drivers = NonMemberCreateInputSerializer(many=True)
    owner = NonMemberOrCompanyCreateInputSerializer()
    vehicle = VehicleWithChassisInputSerializer()

    def validate_drivers(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one driver is required")
        return value

    def validate(self, data):
        if TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM in data.get("insurance_options") and not data.get(
            "max_coverage"
        ):
            raise serializers.ValidationError(
                "If 'reeds afgesloten omnium afdekken' is chosen max_coverage is required"
            )
        elif TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM not in data.get("insurance_options") and data.get(
            "max_coverage"
        ):
            raise serializers.ValidationError(
                "If 'reeds afgesloten omnium afdekken' is not chosen max_coverage is not allowed to be given"
            )

        if TemporaryVehicleInsuranceOptionApi.COVER_OMNIUM in data.get(
            "insurance_options"
        ) and TemporaryVehicleInsuranceOptionApi.OMNIUM in data.get("insurance_options"):
            raise serializers.ValidationError("'reeds afgesloten omnium afdekken' and 'omnium' are mutually exclusive")
        return data


class TravelAssistanceInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    participants = NonMemberNestedOutputSerializer(many=True)
    vehicle = serializers.SerializerMethodField()
    country = CountryOutputSerializer()

    class Meta:
        model = TravelAssistanceInsurance
        fields = base_insurance_detail_fields + ("country", "participants", "vehicle")

    @swagger_serializer_method(serializer_or_field=InuitsVehicleOutputSerializer)
    def get_vehicle(self, obj):
        vehicle = obj.vehicle

        if vehicle:

            inuits_vehicles = InuitsVehicle.objects.filter(
                Q(brand=vehicle.brand) | Q(license_plate=vehicle.license_plate)
            )

            if inuits_vehicles.count() > 0:
                return InuitsVehicleOutputSerializer(inuits_vehicles[0]).data

            return VehicleOutputSerializer(vehicle).data

        return None


class TravelAssistanceInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.by_types([3, 4]))
    vehicle = VehicleInputSerializer(required=False)
    participants = NonMemberCreateInputSerializer(many=True)

    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        return value


class ActivityInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    location = BelgianPostcodeCitySerializer(source="postcode_city")
    group_size = serializers.SerializerMethodField()
    participant_list_file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = ActivityInsurance
        fields = base_insurance_detail_fields + ("nature", "group_size", "location", "participant_list_file")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_group_size(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(GroupSize(obj.group_size))).data

    @swagger_serializer_method(serializer_or_field=ActivityInsuranceAttachmentSerializer)
    def get_participant_list_file(self, obj: ActivityInsurance):
        try:
            attachment: ActivityInsuranceAttachment = obj.attachment

            if attachment:
                return ActivityInsuranceAttachmentSerializer(attachment, context=self.context).data
        except Exception:
            return None


class ActivityInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    group_size = serializers.ChoiceField(choices=GroupSize.choices)
    location = BelgianPostcodeCitySerializer()


class EventInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    location = BelgianPostcodeCitySerializer(source="postcode_city")
    event_size = serializers.SerializerMethodField()
    participant_list_file = serializers.SerializerMethodField(required=False, allow_null=True)

    class Meta:
        model = EventInsurance
        fields = base_insurance_detail_fields + ("nature", "event_size", "location", "participant_list_file")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_event_size(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(EventSize(obj.event_size))).data

    @swagger_serializer_method(serializer_or_field=EventInsuranceAttachmentSerializer)
    def get_participant_list_file(self, obj: EventInsurance):
        try:
            attachment: EventInsuranceAttachment = obj.attachment

            if attachment:
                return EventInsuranceAttachmentSerializer(attachment, context=self.context).data
        except Exception:
            return None


class EventInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    event_size = serializers.ChoiceField(choices=EventSize.choices)
    location = BelgianPostcodeCitySerializer()


class EquipmentInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    postcode_city = BelgianPostcodeCitySerializer()
    equipment = EquipmentNestedOutputSerializer(many=True)
    country = CountryOutputSerializer()

    class Meta:
        model = EquipmentInsurance
        fields = base_insurance_detail_fields + ("nature", "country", "postcode_city", "equipment")


class EquipmentInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.by_type(2), required=False)
    postcode_city = BelgianPostcodeCitySerializer(required=False)
    equipment = EquipmentInputSerializer(many=True)

    def validate_equipment(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one equipment is required")
        return value

    def validate(self, data):
        if not data.get("postcode_city") and not data.get("country"):
            raise serializers.ValidationError("Either postcode_city or country is required")
        elif data.get("postcode_city") and data.get("country"):
            raise serializers.ValidationError("Country and postcode_city are mutually exclusive fields")
        return data
