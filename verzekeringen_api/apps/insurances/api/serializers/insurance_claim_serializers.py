from drf_yasg2.utils import swagger_serializer_method
from rest_framework import serializers
import re

from apps.base.serializers import DateTimeTZField
from apps.files.models import InsuranceClaimAttachment

from apps.members.models import InuitsNonMember
from apps.members.services import GroupAdminMemberService

from apps.members.api.serializers import MemberNestedCreateInputSerializer, NonMemberCreateInputSerializer, \
    GroupAdminMemberDetailOutputSerializer, InuitsNonMemberOutputSerializer
from ...models.insurance_claim import InsuranceClaim


class InsuranceClaimAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaimAttachment
        exclude = ("insurance_claim", "file")


class BaseInsuranceClaimSerializer(serializers.ModelSerializer):
    date_of_accident = DateTimeTZField()
    victim_member = serializers.SerializerMethodField()
    victim_non_member = InuitsNonMemberOutputSerializer()
    activity_type = serializers.JSONField()


    class Meta:
        model = InsuranceClaim
        fields = (
            "id",
            "date",
            "declarant",
            "date_of_accident",
            "activity",
            "activity_type",
            "victim_member",
            "victim_non_member"
        )

    @swagger_serializer_method(serializer_or_field=GroupAdminMemberDetailOutputSerializer)
    def get_victim_member(self, obj):
        if not obj.victim_member_group_admin_id:
            return None
        request = self.context.get("request", None)
        return GroupAdminMemberDetailOutputSerializer(
            GroupAdminMemberService.group_admin_member_detail(
                active_user=request.user, group_admin_id=obj.victim_member_group_admin_id
            )
        ).data


class InsuranceClaimDetailOutputSerializer(BaseInsuranceClaimSerializer):
    date = DateTimeTZField()
    date_of_accident = DateTimeTZField()
    attachment = InsuranceClaimAttachmentSerializer()

    class Meta:
        model = InsuranceClaim
        fields = ("__all__")


class InsuranceClaimInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceClaim
        exclude = (
            "date",
            "declarant",
            "group_number"
        )

    class InsuranceClaimNonMemberRelatedField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            request = self.context.get("request", None)
            queryset = InuitsNonMember.objects.all().allowed(request.user)
            return queryset

    group = serializers.CharField(source="group_id")
    victim_member = serializers.CharField(required=False, allow_null=True)
    victim_non_member = InsuranceClaimNonMemberRelatedField(required=False, allow_null=True)
    activity_type = serializers.JSONField()
    bank_account = serializers.CharField(required=False, allow_null=True)

    def validate_bank_account(self, value):
        pattern = re.compile('^BE[0-9]{14}$')
        if not re.match(pattern, value):
            raise serializers.ValidationError("Invalid bank account number format. It has to be: BE68539007547034")
        return value


    def validate_victim_member(self, value):
        # Validate wether membership number of member is valid
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
        return data

