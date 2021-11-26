import logging

from apps.people.models import InuitsNonMember
from apps.people.serializers import InuitsAbstractPersonSerializer


logger = logging.getLogger(__name__)


class InuitsNonMemberSerializer(InuitsAbstractPersonSerializer):
    # id            pk
    # fields from AbstractInuitsPerson

    class Meta:
        model = InuitsNonMember
        fields = "__all__"
