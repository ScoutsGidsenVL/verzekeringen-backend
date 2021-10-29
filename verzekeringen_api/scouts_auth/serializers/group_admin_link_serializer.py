from rest_framework import serializers

from scouts_auth.models import GroupAdminLink


class GroupAdminLinkSerializer(serializers.Serializer):

    rel: str = serializers.CharField(default="", required=False)
    href: str = serializers.CharField(default="", required=False)
    method: str = serializers.CharField(default="", required=False)
    sections: list = None

    class Meta:
        model = GroupAdminLink
        fields = "__all__"
