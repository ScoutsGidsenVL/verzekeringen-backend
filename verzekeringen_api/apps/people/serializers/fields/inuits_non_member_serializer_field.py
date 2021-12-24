import logging

from rest_framework import serializers

from apps.people.models import InuitsNonMember
from apps.people.serializers import InuitsNonMemberSerializer


logger = logging.getLogger(__name__)


# Special filter field so we can get allowed in queryset
class InuitsNonMemberSerializerField(serializers.PrimaryKeyRelatedField):
    serialize = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, read_only=False, **kwargs)

    def get_queryset(self):
        request = self.context.get("request", None)

        if not request:
            logger.warn("Request not set on parent serializer !")
            return None

        # Return all members for this field, assuming that validation has occured earlier.
        # return InuitsNonMember.objects.all().allowed(request.user)
        return InuitsNonMember.objects.all()

    def to_internal_value(self, data: any) -> dict:
        if isinstance(data, dict):
            data = data.get("id")
        # logger.debug("NON MEMBER pk: %s", data)
        data = super().to_internal_value(data)
        # logger.debug("NON MEMBER DATA: %s", data)

        return data

    def to_representation(self, pk) -> dict:
        logger.debug("PK: %s (type: %s)", pk, type(pk))
        return InuitsNonMemberSerializer().to_representation(InuitsNonMember.objects.get(pk=str(pk)))

    def validate(self, data: dict) -> InuitsNonMember:
        return InuitsNonMember(**data)
