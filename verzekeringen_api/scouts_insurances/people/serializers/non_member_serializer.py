from rest_framework import serializers

from scouts_insurances.people.models import NonMember


class NonMemberSerializer(serializers.ModelSerializer):
    # id            pk
    # last_name     max_length=25       required
    # first_name    max_length=15       required
    # phone_number  max_length=15       optional
    # birth_date    date                optional
    # street        max_length=100      optional
    # number        max_length=5        optional
    # letter_box    max_length=5        optional
    # postal_code                       optional
    # city          max_length=40       optional
    # comment       max_length=500      optional

    class Meta:
        model = NonMember
        fields = "__all__"

    def validate(self, data):
        # Either company_name or first_name, last_name should be given
        if not data.get("company_name") and not (data.get("first_name") and data.get("last_name")):
            raise serializers.ValidationError("If company_name not given first_name and last_name are required")
        elif data.get("company_name") and (data.get("first_name") or data.get("last_name")):
            raise serializers.ValidationError("If company_name given first_name and last_name are not allowed")
        return data
