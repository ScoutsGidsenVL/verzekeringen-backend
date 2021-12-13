import logging

from rest_framework import serializers

from scouts_auth.groupadmin.services import GroupAdmin


logger = logging.getLogger(__name__)


class AbstractScoutsGroupSerializerField(serializers.Field):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, group_group_admin_id: str) -> dict:
        return GroupAdmin().get_group(
            active_user=self.context["request"].user, group_group_admin_id=group_group_admin_id
        )

    def to_representation(self, group_group_admin_id: str) -> dict:
        return GroupAdmin().get_group_serialized(
            active_user=self.context["request"].user, group_group_admin_id=group_group_admin_id
        )
