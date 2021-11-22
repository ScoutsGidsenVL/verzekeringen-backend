import logging, re

from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDict
from rest_framework import serializers

from apps.base.serializers import DateTimeTZField
from apps.members.models import InuitsNonMember
from apps.insurances.models import InsuranceClaim, InsuranceClaimVictim, InsuranceClaimAttachment
from apps.insurances.api.serializer_extensions import PermissionRequiredField

from groupadmin.serializers import ScoutsGroupSerializer, ScoutsMemberSerializer
from groupadmin.services import GroupAdmin

from inuits.models import Gender


logger = logging.getLogger(__name__)


class InsuranceClaimCreateDataSerializer(serializers.Serializer):

    permitted_scouts_groups = ScoutsGroupSerializer(many=True)


class InsuranceClaimAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaimAttachment
        exclude = ("insurance_claim", "file")


class InsuranceClaimVictimOutputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaimVictim
        fields = ["id", "first_name", "last_name"]


class InsuranceClaimVictimOutputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaimVictim
        fields = "__all__"


class InsuranceClaimVictimInputSerializer(serializers.Serializer):
    class Meta:
        fields = "__all__"

    class InsuranceClaimNonMemberRelatedField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            request = self.context.get("request", None)
            queryset = InuitsNonMember.objects.all().allowed(request.user)
            return queryset

    last_name = serializers.CharField()
    first_name = serializers.CharField()
    birth_date = serializers.DateField()
    street = serializers.CharField()
    number = serializers.CharField()
    letter_box = serializers.CharField(required=False)
    # Making postcode int field is bad practice but keeping it because of compatibility with actual NonMember
    postcode = serializers.IntegerField()
    city = serializers.CharField()
    email = serializers.EmailField()
    legal_representative = serializers.CharField(required=False)
    gender = serializers.ChoiceField(required=False, choices=Gender.choices, default=Gender.UNKNOWN)

    group_admin_id = serializers.CharField(required=False, allow_null=True)
    non_member = InsuranceClaimNonMemberRelatedField(required=False, allow_null=True)

    def validate_group_admin_id(self, value):
        # Validate whether membership number of member is valid
        request = self.context.get("request", None)
        try:
            if value:
                GroupAdmin().get_member_info(active_user=request.user, group_admin_id=value)
        except:
            raise serializers.ValidationError("Invalid member id given")
        return value

    def validate(self, data):
        if data.get("victim_member_id") and data.get("victim_non_member"):
            raise serializers.ValidationError("Victim cannot be member and non member at same time")

        return InsuranceClaimVictim(**data)


class BaseInsuranceClaimSerializer(serializers.ModelSerializer):
    date_of_accident = DateTimeTZField()
    activity_type = serializers.JSONField()
    victim = InsuranceClaimVictimOutputListSerializer()
    group_group_admin_id = serializers.CharField()
    declarant = serializers.SerializerMethodField()
    group = serializers.SerializerMethodField()
    note = PermissionRequiredField(
        permission="insurances.view_insuranceclaim_note", field=serializers.CharField(max_length=1024), required=False
    )
    case_number = PermissionRequiredField(
        permission="insurances.view_insuranceclaim_case_number",
        field=serializers.CharField(max_length=30),
        required=False,
    )

    class Meta:
        model = InsuranceClaim
        fields = (
            "id",
            "date",
            "declarant",
            "date_of_accident",
            "activity",
            "activity_type",
            "victim",
            "group_group_admin_id",
            "group",
            "note",
            "case_number",
        )

    def get_declarant(self, object: InsuranceClaim):
        data = GroupAdmin().get_member_info(
            active_user=self.context["request"].user, group_admin_id=object.declarant.group_admin_id
        )
        return ScoutsMemberSerializer(data).data

    def get_group(self, obj: InsuranceClaim):
        return ScoutsGroupSerializer(
            GroupAdmin().get_group(self.context.get("request").user, obj.group_group_admin_id)
        ).data


class InsuranceClaimInputSerializer(serializers.ModelSerializer):

    group_group_admin_id = serializers.CharField()
    activity_type = serializers.JSONField()
    bank_account = serializers.CharField(required=False, allow_null=True)
    victim = InsuranceClaimVictimInputSerializer()
    note = PermissionRequiredField(
        permission="insurances.view_insuranceclaim_note", field=serializers.CharField(max_length=1024), required=False
    )
    case_number = PermissionRequiredField(
        permission="insurances.view_insuranceclaim_case_number",
        field=serializers.CharField(max_length=30),
        required=False,
    )

    class Meta:
        model = InsuranceClaim
        exclude = ("date", "declarant")

    def create(self, validated_data):
        # Create insurance claim
        try:
            insurance_claim = InsuranceClaim.objects.create(id=validated_data.get("id", None))
        except Exception:
            raise ValidationError(detail={"message": "The request is not acceptable."}, code=406)
        logger.debug("attachments")
        if "attachments" in self.context:  # checking if key is in context
            files: MultiValueDict = self.context["attachments"]
            for file in files.getlist("file"):
                InsuranceClaimAttachment.objects.create(insurance_claim=insurance_claim, file=file)

        return insurance_claim

    def validate_bank_account(self, value):
        pattern = re.compile("^BE[0-9]{14}$")
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid bank account number format. It has to be: BE68539007547034")
        return value


class InsuranceClaimDetailOutputSerializer(BaseInsuranceClaimSerializer):
    date = DateTimeTZField()
    date_of_accident = DateTimeTZField()
    # file = InsuranceClaimAttachmentSerializer()
    victim = InsuranceClaimVictimOutputDetailSerializer()
    group = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceClaim
        fields = "__all__"

    def get_group(self, obj: InsuranceClaim):
        return ScoutsGroupSerializer(
            GroupAdmin().get_group(self.context.get("request").user, obj.group_group_admin_id)
        ).data
