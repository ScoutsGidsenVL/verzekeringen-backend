from rest_framework import serializers
from ...models import Member


# Output
class MemberNestedOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = ("id", "last_name", "first_name", "phone_number", "birth_date", "membership_number", "email")


# Input
class MemberNestedCreateInputSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=25)
    first_name = serializers.CharField(max_length=15)
    phone_number = serializers.CharField(max_length=15)
    email = serializers.EmailField(max_length=60)
    birth_date = serializers.DateField()
    membership_number = serializers.IntegerField()
