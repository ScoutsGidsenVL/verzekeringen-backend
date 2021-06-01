from rest_framework import serializers
from ...models import Member, NonMember, InuitsNonMember
from .location_serializers import BelgianPostcodeCityOutputSerializer, BelgianPostcodeCityInputSerializer


# Output
class MemberNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "last_name", "first_name", "phone_number", "birth_date", "membership_number", "email")


class NonMemberNestedOutputSerializer(serializers.ModelSerializer):
    postcode_city = BelgianPostcodeCityOutputSerializer()

    class Meta:
        model = NonMember
        fields = (
            "last_name",
            "first_name",
            "phone_number",
            "birth_date",
            "street",
            "number",
            "letter_box",
            "postcode_city",
            "comment",
        )


class InuitsNonMemberOutputSerializer(serializers.ModelSerializer):
    postcode_city = BelgianPostcodeCityOutputSerializer()

    class Meta:
        model = InuitsNonMember
        fields = (
            "last_name",
            "first_name",
            "phone_number",
            "birth_date",
            "street",
            "number",
            "letter_box",
            "postcode_city",
            "comment",
        )


# Input
class MemberNestedCreateInputSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=25)
    first_name = serializers.CharField(max_length=15)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(max_length=60)
    birth_date = serializers.DateField()
    membership_number = serializers.IntegerField()


class NonMemberCreateInputSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=25)
    first_name = serializers.CharField(max_length=15)
    phone_number = serializers.CharField(max_length=15)
    birth_date = serializers.DateField()
    street = serializers.CharField(max_length=100)
    number = serializers.CharField(max_length=5)
    letter_box = serializers.CharField(max_length=5, required=False, allow_blank=True)
    comment = serializers.CharField(max_length=500, required=False, allow_blank=True)
    postcode_city = BelgianPostcodeCityInputSerializer()


class InuitsNonMemberCreateInputSerializer(NonMemberCreateInputSerializer):
    group = serializers.CharField(source="group_id")
