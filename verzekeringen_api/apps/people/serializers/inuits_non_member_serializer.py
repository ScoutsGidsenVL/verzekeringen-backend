import logging

from rest_framework import serializers

from apps.people.models import InuitsNonMember

from scouts_auth.inuits.serializers import InuitsPersonSerializer


logger = logging.getLogger(__name__)


class InuitsNonMemberSerializer(InuitsPersonSerializer, serializers.ModelSerializer):
    # id            pk
    # fields from InuitsPerson
    # comment       max_length=500      optional

    class Meta:
        model = InuitsNonMember
        fields = "__all__"

    def to_internal_value(self, data):
        logger.debug("DATA: %s", data)

        group_admin_id = data.pop("group_group_admin_id", None)
        if group_admin_id:
            logger.warn("Discarding irrelevent group admin id for non-member")

        return data
