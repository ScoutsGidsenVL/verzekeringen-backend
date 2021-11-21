import logging

from groupadmin.models import (
    ScoutsMemberListMember,
    ScoutsMemberListResponse,
)
from groupadmin.serializers import ScoutsValueSerializer, ScoutsLinkSerializer, ScoutsResponseSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsMemberListMemberSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "index": data.pop("positie", None),
            "values": ScoutsValueSerializer(many=True).to_internal_value(list(data.pop("waarden", {}).items())),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", [])),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> ScoutsMemberListMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberListMember:
        if validated_data is None:
            return None

        instance = ScoutsMemberListMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.index = validated_data.pop("index", None)
        instance.values = ScoutsValueSerializer(many=True).create(validated_data.pop("values", {}))
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsMemberListResponseSerializer(ScoutsResponseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "members": ScoutsMemberListMemberSerializer(many=True).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", str(remaining_keys))

        return validated_data

    def save(self) -> ScoutsMemberListResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberListResponse:
        if validated_data is None:
            return None

        instance = ScoutsMemberListResponse()

        instance.members = ScoutsMemberListMemberSerializer(many=True).create(validated_data.pop("members", []))

        super().create(validated_data)

        logger.debug("INSTANCE: %s", instance)

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance