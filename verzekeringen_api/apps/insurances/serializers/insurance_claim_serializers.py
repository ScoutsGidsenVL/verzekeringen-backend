import logging, re

from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDict
from rest_framework import serializers

from apps.people.serializers import InuitsClaimVictimSerializer
from apps.insurances.models import InsuranceClaim, InsuranceClaimAttachment

from scouts_auth.groupadmin.serializers import AbstractScoutsGroupSerializer, ScoutsUserSerializer
from scouts_auth.groupadmin.serializers.fields import AbstractScoutsGroupSerializerField
from scouts_auth.groupadmin.services import GroupAdmin

from scouts_auth.inuits.serializers import PermissionRequiredField


logger = logging.getLogger(__name__)


class InsuranceClaimCreateDataSerializer(serializers.Serializer):

    permitted_scouts_groups = AbstractScoutsGroupSerializer(many=True)


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

    activity_type = serializers.JSONField()
    victim = InuitsClaimVictimSerializer()
    declarant = ScoutsUserSerializer(required=False)
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
        exclude = []

    # @TODO see if adding the group can't be done with a AbstractScoutsGroupSerializerField
    def to_representation(self, data: dict) -> dict:
        data = super().to_representation(data)

        data["group"] = GroupAdmin().get_group_serialized(
            active_user=self.context.get("request").user, group_group_admin_id=data.get("group_group_admin_id")
        )

        return data

    def get_activity_type(self, obj: InsuranceClaim) -> str:
        return obj.activity_type

    def create(self, validated_data: dict) -> InsuranceClaim:
        try:
            insurance_claim = InsuranceClaim.objects.create(id=validated_data.get("id", None))
        except Exception:
            raise ValidationError(detail={"message": "The request is not acceptable."}, code=406)

        logger.debug("attachments")
        if "attachments" in self.context:  # checking if key is in context
            files: MultiValueDict = self.context["attachments"]
            for file in files.getlist("file"):
                print('@@@@@FILE@@@@@: ', file)
                InsuranceClaimAttachment.objects.create(insurance_claim=insurance_claim, file=file)

        return insurance_claim

    def validate_bank_account(self, value):
        pattern = re.compile("^BE[0-9]{14}$")
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid bank account number format. It has to be: BE68539007547034")
        return value
