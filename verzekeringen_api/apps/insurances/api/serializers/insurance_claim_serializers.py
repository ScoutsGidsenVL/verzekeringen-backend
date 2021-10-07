import re

from rest_framework import serializers

from apps.base.serializers import DateTimeTZField
from apps.members.api.serializers import GroupAdminMemberListOutputSerializer
from apps.members.enums import Sex
from apps.members.models import InuitsNonMember
from apps.members.services import GroupAdminMemberService
from apps.members.services.group_admin_member_service import group_admin_member_detail
from apps.scouts_auth.api.serializers import GroupOutputSerializer
from apps.insurances.models import InsuranceClaim, InsuranceClaimVictim, InsuranceClaimAttachment
from . import InsuranceClaimAdmistrativeFieldsMixin


class InsuranceClaimAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaimAttachment
        exclude = ("insurance_claim", "file")


class InsuranceClaimVictimOutputListSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaimVictim
        fields = ["id", "first_name", "last_name"]


class BaseInsuranceClaimSerializer(InsuranceClaimAdmistrativeFieldsMixin, serializers.ModelSerializer):
    date_of_accident = DateTimeTZField()
    activity_type = serializers.JSONField()
    victim = InsuranceClaimVictimOutputListSerializer()
    group = GroupOutputSerializer()
    declarant = serializers.SerializerMethodField()

    class Meta:
        model = InsuranceClaim
        fields = (
            "id",
            "group_number",
            "date",
            "declarant",
            "declarant",
            "date_of_accident",
            "activity",
            "activity_type",
            "victim",
            "group",
            "note",
            "case_number",
        )

    def get_declarant(self, object: InsuranceClaim):
        data = group_admin_member_detail(
            active_user=self.context["request"].user, group_admin_id=object.declarant.group_admin_id
        )
        return GroupAdminMemberListOutputSerializer(data).data


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
    sex = serializers.ChoiceField(required=False, choices=Sex.choices, default=Sex.UNKNOWN)

    group_admin_id = serializers.CharField(required=False, allow_null=True)
    non_member = InsuranceClaimNonMemberRelatedField(required=False, allow_null=True)

    def validate_group_admin_id(self, value):
        # Validate whether membership number of member is valid
        request = self.context.get("request", None)
        try:
            if value:
                GroupAdminMemberService.group_admin_member_detail(active_user=request.user, group_admin_id=value)
        except:
            raise serializers.ValidationError("Invalid member id given")
        return value

    def validate(self, data):
        if data.get("victim_member_id") and data.get("victim_non_member"):
            raise serializers.ValidationError("There can only be one max victim")
        return InsuranceClaimVictim(**data)


class InsuranceClaimDetailOutputSerializer(BaseInsuranceClaimSerializer):
    date = DateTimeTZField()
    date_of_accident = DateTimeTZField()
    attachment = InsuranceClaimAttachmentSerializer()
    victim = InsuranceClaimVictimOutputDetailSerializer()

    class Meta:
        model = InsuranceClaim
        fields = "__all__"


class InsuranceClaimInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        exclude = ("date", "declarant", "group_number")

    group = serializers.CharField(source="group_id")
    activity_type = serializers.JSONField()
    bank_account = serializers.CharField(required=False, allow_null=True)
    victim = InsuranceClaimVictimInputSerializer()
    file = serializers.FileField()

    def validate_bank_account(self, value):
        pattern = re.compile("^BE[0-9]{14}$")
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid bank account number format. It has to be: BE68539007547034")
        return value
