from rest_framework import serializers

from scouts_auth.models import GroupAdminLink


class GroupAdminLinkSerializer(serializers.Serializer):

    rel: str = serializers.CharField(default="")
    href: str = serializers.CharField(default="")
    method: str = serializers.CharField(default="")
    sections: list

    class Meta:
        model = GroupAdminLink
        fields = "__all__"
