from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method
from django.conf import settings
from apps.base.serializers import EnumOutputSerializer
from apps.base.helpers import parse_choice_to_tuple
from apps.scouts_auth.api.serializers import GroupOutputSerializer
from apps.members.api.serializers import (
    MemberNestedOutputSerializer,
    MemberNestedCreateInputSerializer,
    NonMemberNestedOutputSerializer,
    NonMemberCompanyNestedOutputSerializer,
    NonMemberCreateInputSerializer,
    NonMemberOrCompanyCreateInputSerializer,
)
from apps.locations.api.serializers import (
    BelgianPostcodeCityOutputSerializer,
    BelgianPostcodeCityInputSerializer,
    CountryOutputSerializer,
)
from apps.locations.models import Country
from apps.equipment.api.serializers import (
    VehicleOutputSerializer,
    VehicleInputSerializer,
    VehicleWithChassisOutputSerializer,
    VehicleWithChassisInputSerializer,
)
from .insurance_type_serializers import InsuranceTypeOutputSerializer
from ...models import (
    BaseInsurance,
    ActivityInsurance,
    TemporaryInsurance,
    TravelAssistanceInsurance,
    InsuranceType,
    TemporaryVehicleInsurance,
    EventInsurance,
)
from ...models.enums import (
    InsuranceStatus,
    GroupSize,
    EventSize,
    TemporaryVehicleInsuranceOption,
    TemporaryVehicleInsuranceOptionApi,
    TemporaryVehicleInsuranceCoverageOption,
)


# Output
class InsuranceListOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    group = GroupOutputSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)

    class Meta:
        model = BaseInsurance
        fields = ("id", "status", "type", "group", "start_date", "end_date", "responsible_member")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data


# Just some a tuple so we dont need to copy everything (cannot use inheritance because Meta does not get inherited)
base_insurance_detail_fields = (
    "id",
    "status",
    "type",
    "group",
    "start_date",
    "end_date",
    "responsible_member",
    "total_cost",
    "created_on",
    "comment",
    "vvks_comment",
)


class BaseInsuranceDetailOutputSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    type = InsuranceTypeOutputSerializer(read_only=True)
    group = GroupOutputSerializer(read_only=True)
    responsible_member = MemberNestedOutputSerializer(read_only=True)

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_status(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(InsuranceStatus(obj.status))).data


class ActivityInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    location = BelgianPostcodeCityOutputSerializer(source="postcode_city")
    group_size = serializers.SerializerMethodField()

    class Meta:
        model = ActivityInsurance
        fields = base_insurance_detail_fields + ("nature", "group_size", "location")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_group_size(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(GroupSize(obj.group_size))).data


class TemporaryInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    postcode_city = BelgianPostcodeCityOutputSerializer()
    non_members = NonMemberNestedOutputSerializer(many=True)
    country = CountryOutputSerializer()

    class Meta:
        model = TemporaryInsurance
        fields = base_insurance_detail_fields + ("nature", "country", "postcode_city", "non_members")


class TravelAssistanceInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    participants = NonMemberNestedOutputSerializer(many=True)
    vehicle = VehicleOutputSerializer(read_only=True)
    country = CountryOutputSerializer()

    class Meta:
        model = TravelAssistanceInsurance
        fields = base_insurance_detail_fields + ("country", "participants", "vehicle")


class TemporaryVehicleInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    drivers = NonMemberNestedOutputSerializer(many=True)
    owner = serializers.SerializerMethodField()
    vehicle = VehicleWithChassisOutputSerializer(read_only=True)
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


class EventInsuranceDetailOutputSerializer(BaseInsuranceDetailOutputSerializer):
    location = BelgianPostcodeCityOutputSerializer(source="postcode_city")
    event_size = serializers.SerializerMethodField()

    class Meta:
        model = EventInsurance
        fields = base_insurance_detail_fields + ("nature", "event_size", "location")

    @swagger_serializer_method(serializer_or_field=EnumOutputSerializer)
    def get_event_size(self, obj):
        return EnumOutputSerializer(parse_choice_to_tuple(EventSize(obj.event_size))).data


# Input
class BaseInsuranceCreateInputSerializer(serializers.Serializer):
    group = serializers.CharField(source="group_id", max_length=6)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    responsible_phone_number = serializers.CharField(max_length=15, required=False)


class ActivityInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    group_size = serializers.ChoiceField(choices=GroupSize.choices)
    location = BelgianPostcodeCityInputSerializer()


class TemporaryInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.by_type(2), required=False)
    postcode_city = BelgianPostcodeCityInputSerializer(required=False)
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


class TravelAssistanceInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    country = serializers.PrimaryKeyRelatedField(queryset=Country.objects.by_types([3, 4]))
    vehicle = VehicleInputSerializer(required=False)
    participants = NonMemberCreateInputSerializer(many=True)

    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        return value


class EventInsuranceCreateInputSerializer(BaseInsuranceCreateInputSerializer):
    nature = serializers.CharField(max_length=500)
    event_size = serializers.ChoiceField(choices=EventSize.choices)
    location = BelgianPostcodeCityInputSerializer()
