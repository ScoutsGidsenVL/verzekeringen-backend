import logging, re

from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDict
from rest_framework import serializers

from apps.people.serializers import InuitsClaimVictimSerializer
from apps.insurances.models import InsuranceClaim, InsuranceClaimAttachment

from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer, ScoutsMemberSerializer
from scouts_auth.groupadmin.services import GroupAdmin

from scouts_auth.inuits.serializers import DateTimeTimezoneField, PermissionRequiredField


logger = logging.getLogger(__name__)


class InsuranceClaimCreateDataSerializer(serializers.Serializer):

    permitted_scouts_groups = ScoutsGroupSerializer(many=True)


# class BaseInsuranceClaimSerializer(serializers.ModelSerializer):
#     date_of_accident = DateTimeTimezoneField()
#     activity_type = serializers.JSONField()
#     victim = InuitsClaimVictimSerializer(many=True)
#     group_group_admin_id = serializers.CharField()
#     declarant = serializers.SerializerMethodField()
#     group = serializers.SerializerMethodField()
#     note = PermissionRequiredField(
#         permission="insurances.view_insuranceclaim_note", field=serializers.CharField(max_length=1024), required=False
#     )
#     case_number = PermissionRequiredField(
#         permission="insurances.view_insuranceclaim_case_number",
#         field=serializers.CharField(max_length=30),
#         required=False,
#     )

#     class Meta:
#         model = InsuranceClaim
#         fields = (
#             "id",
#             "date",
#             "declarant",
#             "date_of_accident",
#             "activity",
#             "activity_type",
#             "victim",
#             "group_group_admin_id",
#             "group",
#             "note",
#             "case_number",
#         )

#     def get_declarant(self, object: InsuranceClaim):
#         data = GroupAdmin().get_member_info(
#             active_user=self.context["request"].user, group_admin_id=object.declarant.group_admin_id
#         )
#         return ScoutsMemberSerializer(data).data

#     def get_group(self, obj: InsuranceClaim):
#         return ScoutsGroupSerializer(
#             GroupAdmin().get_group(self.context.get("request").user, obj.group_group_admin_id)
#         ).data


class InsuranceClaimSerializer(serializers.ModelSerializer):
    # group_group_admin_id          max_length=6        optional
    # date_of_accident              date                optional
    # declarant                     ScoutsUser          optional
    # victim                        InuitsClaimVictim   optional
    # bank_account                  max_length=30       optional
    # location                      max_length=128      optional
    # activity                      max_length=1024     optional
    # used_transport                max_length=30       optional
    # description                   max_length=1024     required

    # activity_type = JSONField(max_length=128)
    # damage_type = OptionalCharField(max_length=128)

    # involved_party_name           max_length=1024     optional
    # involved_party_description    max_length=1024     optional
    # involved_party_birthdate      date                optional

    # official_report_description   max_length=1024     optional
    # pv_number                     max_length=30       optional

    # witness_name                  max_length=128      optional
    # witness_description           max_length=1024     optional

    # leadership_description        max_length=1024     optional

    # note                          max_length=1024     optional
    # case_number                   max_length=30       optional

    # group_group_admin_id = serializers.CharField()
    # activity_type = serializers.JSONField()
    # bank_account = serializers.CharField(required=False, allow_null=True)
    activity_type = serializers.JSONField()
    victim = InuitsClaimVictimSerializer()
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
        exclude = ["declarant"]

    def get_activity_type(self, obj: InsuranceClaim) -> str:
        return obj.activity_type

    def create(self, validated_data: dict) -> InsuranceClaim:
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


# class InsuranceClaimSerializer(BaseInsuranceClaimSerializer):
#     date = DateTimeTimezoneField()
#     date_of_accident = DateTimeTimezoneField()
#     victim = InuitsClaimVictimSerializer(many=True)
#     group = serializers.SerializerMethodField()
#     attachment = serializers.SerializerMethodField()

#     class Meta:
#         model = InsuranceClaim
#         fields = "__all__"

#     def get_group(self, obj: InsuranceClaim):
#         return ScoutsGroupSerializer(
#             GroupAdmin().get_group(self.context.get("request").user, obj.group_group_admin_id)
#         ).data

#     def get_attachment(self, obj: InsuranceClaim):
#         attachment: InsuranceClaimAttachment = obj.attachment

#         if attachment:
#             return InsuranceClaimAttachmentSerializer(attachment).data

#         return None
