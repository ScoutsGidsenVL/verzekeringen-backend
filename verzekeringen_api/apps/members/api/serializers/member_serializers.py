from rest_framework import serializers
from apps.locations.api.serializers import BelgianPostcodeCityOutputSerializer, BelgianPostcodeCityInputSerializer
from ...models import Member, NonMember, InuitsNonMember


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


class GroupAdminMemberListOutputSerializer(serializers.Serializer):
    id = serializers.CharField(source="group_admin_id")
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.EmailField()
    birth_date = serializers.DateField()
    group_admin_id = serializers.CharField()


class GroupAdminMemberDetailOutputSerializer(GroupAdminMemberListOutputSerializer):
    membership_number = serializers.CharField()
    street = serializers.CharField(source="address.street")
    number = serializers.CharField(source="address.number")
    letter_box = serializers.CharField(source="address.letter_box")
    postcode_city = BelgianPostcodeCityOutputSerializer(source="address.postcode_city")


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
