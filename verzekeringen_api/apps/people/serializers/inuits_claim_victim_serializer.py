import logging

from rest_framework import serializers

from apps.people.models import InuitsClaimVictim
from apps.people.serializers.fields import InuitsNonMemberSerializerField

from scouts_auth.inuits.serializers import InuitsPersonSerializer
from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class InuitsClaimVictimSerializer(InuitsPersonSerializer):
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

    # Removed from model and serializers, since it isn't used
    # non_member            InuitsNonMember         optional
    # non_member = InuitsNonMemberSerializerField(required=False, allow_null=True)

    class Meta:
        model = InuitsClaimVictim
        fields = "__all__"

    # def validate_group_admin_id(self, group_admin_id: str) -> str:
    #     if not group_admin_id or len(group_admin_id.strip()) == 0:
    #         raise serializers.ValidationError("Can't validate victim without a group admin id")

    #     # Validate whether membership number of member is valid
    #     victim: AbstractScoutsMember = None
    #     try:
    #         # logger.debug("Validating claim victim as scouts member with group admin id %s", group_admin_id)
    #         victim = GroupAdmin().get_member_info(
    #             active_user=self.context["request"].user, group_admin_id=group_admin_id
    #         )

    #         if not victim or victim.group_admin_id != group_admin_id:
    #             victim = None
    #     except:
    #         raise serializers.ValidationError("Couldn't validate victim with group admin id {}".format(group_admin_id))

    #     if victim is None:
    #         raise serializers.ValidationError(
    #             "Victim with group admin id {} not found by groupadmin".format(group_admin_id)
    #         )

    #     return group_admin_id

    def validate(self, data: dict) -> InuitsClaimVictim:
        return InuitsClaimVictim(**data)
