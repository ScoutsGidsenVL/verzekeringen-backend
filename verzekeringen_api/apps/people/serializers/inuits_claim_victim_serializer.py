import logging

from rest_framework import serializers

from apps.people.models import InuitsClaimVictim, InuitsNonMember
from apps.people.serializers import InuitsAbstractPersonSerializer

from groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsClaimVictimSerializer(InuitsAbstractPersonSerializer):
    # id                    pk
    # first_name            max_length=15           required
    # last_name             max_length=25           required
    # phone_number          max_length=15           optional
    # birth_date            date                    optional
    # gender                choices=Gender.choices  optional
    # street                max_length=100          optional
    # number                max_length=5            optional
    # letter_box            max_length=5            optional
    # postal_code           integer                 optional
    # city                  max_length=40           optional
    # comment               max_length=500          optional
    # legal_representative  max_length=128          optional
    # group_admin_id        max_length=255          optional
    # #
    # non_member = models.ForeignKey(
    #     InuitsNonMember,
    #     null=True,
    #     related_name="claim_victim",
    #     blank=True,
    #     on_delete=models.SET_NULL,
    # )

    class Meta:
        model = InuitsClaimVictim
        fields = "__all__"

    class InsuranceClaimNonMemberRelatedField(serializers.PrimaryKeyRelatedField):
        def get_queryset(self):
            request = self.context.get("request", None)
            queryset = InuitsNonMember.objects.all().allowed(request.user)
            return queryset

    # last_name = serializers.CharField()
    # first_name = serializers.CharField()
    # birth_date = serializers.DateField()
    # street = serializers.CharField()
    # number = serializers.CharField()
    # letter_box = serializers.CharField(required=False)
    # # Making postal_code int field is bad practice but keeping it because of compatibility with actual NonMember
    # postal_code = serializers.IntegerField()
    # city = serializers.CharField()
    # email = serializers.EmailField()
    # legal_representative = serializers.CharField(required=False)
    # gender = serializers.ChoiceField(required=False, choices=Gender.choices, default=Gender.UNKNOWN)

    # group_admin_id = serializers.CharField(required=False, allow_null=True)
    non_member = InsuranceClaimNonMemberRelatedField(required=False, allow_null=True)

    def validate_group_admin_id(self, value: str) -> str:
        logger.debug("Validating group_admin_id for claim victim (group_admin_id: %s)", value)
        # Validate whether membership number of member is valid
        request = self.context.get("request", None)
        try:
            if value:
                GroupAdmin().get_member_info(active_user=request.user, group_admin_id=value)
        except:
            raise serializers.ValidationError("Couldn't validate group_admin_id {} for claim victim".format(value))
        return value

    def validate(self, data):
        if data.get("victim_member_id") and data.get("victim_non_member"):
            raise serializers.ValidationError("Victim cannot be member and non member at same time")

        return InuitsClaimVictim(**data)
