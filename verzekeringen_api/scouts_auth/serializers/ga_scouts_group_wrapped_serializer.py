from typing import List

from rest_framework import serializers

from scouts_auth.models import ScoutsGroup, GroupAdminLink
from scouts_auth.serializers import ScoutsGroupSerializer, GroupAdminLinkSerializer


class ScoutsGroupWrappedSerializer(serializers.Serializer):

    groups: List[ScoutsGroup] = ScoutsGroupSerializer(source="groepen", many=True, default=[])
    links: List[GroupAdminLink] = GroupAdminLinkSerializer(many=True, default=[])
