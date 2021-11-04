import logging
from typing import List

from rest_framework import serializers

from scouts_auth.models import ScoutsGroup, GroupAdminLink, ResponseScoutsGroup
from scouts_auth.serializers import ScoutsGroupSerializer, GroupAdminLinkSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsGroupWrappedSerializer(NonModelSerializer):
    def to_internal_value(self, data) -> dict:
        validated_data = {
            "groups": ScoutsGroupSerializer(many=True).to_internal_value(data.pop("groepen", [])),
            "links": GroupAdminLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def create(self, validated_data) -> ResponseScoutsGroup:
        instance = ResponseScoutsGroup()

        instance.groups = ScoutsGroupSerializer(many=True).create(validated_data.pop("groups", []))
        instance.links = GroupAdminLinkSerializer(many=True).create(validated_data.pop("links", []))

        return instance
