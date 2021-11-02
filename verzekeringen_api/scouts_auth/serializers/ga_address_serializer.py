import logging

from rest_framework import serializers

from scouts_auth.models import GroupAdminAddress


logger = logging.getLogger(__name__)


class GroupAdminAddressSerializer(serializers.Serializer):

    id: str = serializers.CharField(default="")
    street: str = serializers.CharField(source="straat", default="")
    number: str = serializers.CharField(source="nummer", default="")
    letter_box: str = serializers.CharField(source="bus", default="")
    postcode_city = None
    postal_code: str = serializers.CharField(source="postcode", default="")
    city: str = serializers.CharField(source="gemeente", default="")
    country: str = serializers.CharField(source="land", default="")
    phone: str = serializers.CharField(source="telefoon", default="")
    postal_address: bool = serializers.BooleanField(source="postadres", default=False)
    status: str = serializers.CharField(default="")
    position: dict = None
    giscode: str = serializers.CharField(default="")
    description: str = serializers.CharField(source="omschrijving", default="")

    class Meta:
        model = GroupAdminAddress
        fields = "__all__"

    def save(self) -> GroupAdminAddress:
        return self.create(self.validated_data)

    def create(self, **validated_data) -> GroupAdminAddress:
        instance = GroupAdminAddress()

        instance.group_admin_id = validated_data.pop("id", "")
        instance.street = validated_data.pop("straat", "")
        instance.number = validated_data.pop("nummer", "")
        instance.letter_box = validated_data.pop("", "")
        instance.postal_code = validated_data.pop("postcode", "")
        instance.city = validated_data.pop("gemeente", "")
        instance.country = validated_data.pop("land", "")
        instance.phone = validated_data.pop("telefoon", "")
        instance.postal_address = validated_data.pop("postadres", False)
        instance.status = validated_data.pop("status", "")
        instance.position = validated_data.pop("", "")
        instance.giscode = validated_data.pop("giscode", "")
        instance.description = validated_data.pop("omschrijving", "")

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
