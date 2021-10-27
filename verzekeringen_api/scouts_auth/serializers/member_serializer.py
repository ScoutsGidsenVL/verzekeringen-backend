from rest_framework import serializers

from scouts_auth.models import GroupAdminMember

class MemberSerializer(serializers.Serializer):

    class Meta:
        model = GroupAdminMember
        fields = "__all__"
