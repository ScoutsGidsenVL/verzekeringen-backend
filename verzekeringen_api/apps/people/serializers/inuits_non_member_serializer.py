import logging

from rest_framework import serializers

from apps.people.models import InuitsNonMember

from scouts_auth.inuits.serializers import InuitsPersonSerializer


logger = logging.getLogger(__name__)


class InuitsNonMemberSerializer(serializers.ModelSerializer):
    # id            pk
    # fields from InuitsPerson
    # comment       max_length=500      optional

    class Meta:
        model = InuitsNonMember
        fields = "__all__"
