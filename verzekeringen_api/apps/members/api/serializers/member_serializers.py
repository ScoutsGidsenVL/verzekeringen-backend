from rest_framework import serializers
from apps.locations.api.serializers import BelgianPostcodeCityOutputSerializer, BelgianPostcodeCityInputSerializer
from ...models import Member, NonMember, InuitsNonMember


# Output
class MemberNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id",
                  "last_name",
                  "first_name",
                  "phone_number",
                  "birth_date",
                  "membership_number",
                  "email",
                  "group_admin_id")


class NonMemberNestedOutputSerializer(serializers.ModelSerializer):
    postcode_city = BelgianPostcodeCityOutputSerializer()

    class Meta:
        model = NonMember
        fields = (
            "id",
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


class NonMemberCompanyNestedOutputSerializer(serializers.ModelSerializer):
    postcode_city = BelgianPostcodeCityOutputSerializer()
    company_name = serializers.CharField(source="last_name")

    class Meta:
        model = NonMember
        fields = (
            "id",
            "company_name",
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
            "id",
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
    membership_number = serializers.IntegerField()
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
    group_admin_id = serializers.CharField(max_length=255)


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


class NonMemberOrCompanyCreateInputSerializer(NonMemberCreateInputSerializer):
    company_name = serializers.CharField(max_length=25, required=False)
    last_name = serializers.CharField(max_length=25, required=False)
    first_name = serializers.CharField(max_length=15, required=False)

    def validate(self, data):
        # Either company_name or first_name, last_name should be given
        if not data.get("company_name") and not (data.get("first_name") and data.get("last_name")):
            raise serializers.ValidationError("If company_name not given first_name and last_name are required")
        elif data.get("company_name") and (data.get("first_name") or data.get("last_name")):
            raise serializers.ValidationError("If company_name given first_name and last_name are not allowed")
        return data


class InuitsNonMemberCreateInputSerializer(NonMemberCreateInputSerializer):
    group = serializers.CharField(source="group_id")
