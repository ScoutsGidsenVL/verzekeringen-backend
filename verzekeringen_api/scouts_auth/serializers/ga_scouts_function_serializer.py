from typing import List
from datetime import datetime

from rest_framework import serializers

from scouts_auth.models import ScoutsFunction, GroupAdminLink
from scouts_auth.serializers import GroupAdminLinkSerializer

from inuits.logging import InuitsLogger


logger = InuitsLogger(__name__)


class ScoutsFunctionSerializer(serializers.Serializer):

    group: str = serializers.CharField()
    function: str = serializers.CharField()
    begin: datetime = serializers.DateTimeField()
    code: str = serializers.CharField()
    description: str = serializers.CharField()
    links: List[GroupAdminLink]

    # class Meta:
    #     model = ScoutsFunction
    #     fields = "__all__"

    def save(self) -> ScoutsFunction:
        return self.create(self.validated_data)

    def create(self, validated_data) -> ScoutsFunction:
        instance = ScoutsFunction()

        links_serializer = GroupAdminLinkSerializer(data=validated_data.pop("links", []), many=True)
        links_serializer.is_valid(raise_exception=True)
        links = links_serializer.save()

        instance.group = validated_data.pop("groep", "")
        instance.function = validated_data.pop("functie", "")
        instance.begin = validated_data.pop("begin", "")
        instance.code = validated_data.pop("code", "")
        instance.description = validated_data.pop("omschrijving", "")
        instance.links = links

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
