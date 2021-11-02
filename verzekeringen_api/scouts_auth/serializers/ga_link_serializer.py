import logging

from rest_framework import serializers

from scouts_auth.models import GroupAdminLink


logger = logging.getLogger(__name__)


class GroupAdminLinkSerializer(serializers.ModelSerializer):

    # rel: str = serializers.CharField(default="")
    # href: str = serializers.CharField(default="")
    # method: str = serializers.CharField(default="")
    sections: list = serializers.ListField(source="secties", default=[])

    class Meta:
        model = GroupAdminLink
        fields = "__all__"

    def save(self) -> GroupAdminLink:
        return self.create(self.validated_data)

    def create(self, validated_data) -> GroupAdminLink:
        instance = GroupAdminLink()

        instance.rel = validated_data.pop("rel", "")
        instance.href = validated_data.pop("href", "")
        instance.method = validated_data.pop("method", "")
        instance.sections = validated_data.pop("secties", [])

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
