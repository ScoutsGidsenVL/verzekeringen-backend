import logging

from groupadmin.models import ScoutsMemberSearchMember, ScoutsMemberSearchResponse
from groupadmin.serializers import ScoutsLinkSerializer, ScoutsResponseSerializer

from inuits.serializers import NonModelSerializer


logger = logging.getLogger(__name__)


class ScoutsMemberSearchMemberSerializer(NonModelSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "group_admin_id": data.pop("id", None),
            "first_name": data.pop("voornaam", None),
            "last_name": data.pop("achternaam", None),
            "birth_date": data.pop("geboortedatum", None),
            "email": data.pop("email", None),
            "phone": data.pop("gsm", None),
            "links": ScoutsLinkSerializer(many=True).to_internal_value(data.pop("links", None)),
        }

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsMemberSearchMember:
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberSearchMember:
        if validated_data is None:
            return None

        instance = ScoutsMemberSearchMember()

        instance.group_admin_id = validated_data.pop("group_admin_id", None)
        instance.first_name = validated_data.pop("first_name", None)
        instance.last_name = validated_data.pop("last_name", None)
        instance.birth_date = validated_data.pop("birth_date", None)
        instance.email = validated_data.pop("email", None)
        instance.phone = validated_data.pop("phone", None)
        instance.links = ScoutsLinkSerializer(many=True).create(validated_data.pop("links", None))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance


class ScoutsMemberSearchResponseSerializer(ScoutsResponseSerializer):
    def to_internal_value(self, data: dict) -> dict:
        if data is None:
            return None

        validated_data = {
            "members": ScoutsMemberSearchMemberSerializer(many=True).to_internal_value(data.pop("leden", [])),
        }

        validated_data = {**validated_data, **(super().to_internal_value(data))}

        remaining_keys = data.keys()
        if len(remaining_keys) > 0:
            logger.warn("UNPARSED INCOMING JSON DATA KEYS: %s", remaining_keys)

        return validated_data

    def save(self) -> ScoutsMemberSearchResponse:
        self.is_valid(raise_exception=True)
        return self.create(self.validated_data)

    def create(self, validated_data: dict) -> ScoutsMemberSearchResponse:
        if validated_data is None:
            return None

        instance = ScoutsMemberSearchResponse()
        instance = super().update(instance, validated_data)

        instance.members = ScoutsMemberSearchMemberSerializer(many=True).create(validated_data.pop("members", []))

        remaining_keys = validated_data.keys()
        if len(remaining_keys) > 0:
            logger.debug("UNPARSED JSON DATA: %s", str(remaining_keys))

        return instance
