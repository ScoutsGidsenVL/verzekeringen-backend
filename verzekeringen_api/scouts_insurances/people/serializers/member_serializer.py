from rest_framework import serializers

from scouts_auth.inuits.serializers import DatetypeAwareDateSerializerField
from scouts_insurances.people.models import Member


class MemberSerializer(serializers.ModelSerializer):
    # id                    pk
    # first_name            max_length=15               required
    # last_name             max_length=25               required
    # phone_number          max_length=15               optional
    # birth_date            date                        optional
    # membership_number     scouts membership number
    # email                 max_length=60               optional
    # group_admin_id        max_length=255              optional

    birth_date = DatetypeAwareDateSerializerField()

    class Meta:
        model = Member
        fields = "__all__"
