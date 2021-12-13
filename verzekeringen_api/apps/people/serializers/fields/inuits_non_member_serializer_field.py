import logging

from rest_framework import serializers

from apps.people.models import InuitsNonMember
from apps.people.serializers import InuitsNonMemberSerializer


logger = logging.getLogger(__name__)


# Special filter field so we can get allowed in queryset
class InuitsNonMemberSerializerField(serializers.PrimaryKeyRelatedField):
    serialize = True

    def get_queryset(self):
        request = self.context.get("request", None)

        if not request:
            logger.warn("Request not set on parent serializer !")
            return None

        # Return all members for this field, assuming that validation has occured earlier.
        # return InuitsNonMember.objects.all().allowed(request.user)
        return InuitsNonMember.objects.all()

    def to_internal_value(self, pk) -> dict:
        return super().to_internal_value(pk)

    def to_representation(self, pk) -> dict:
        logger.debug("PK: %s (type: %s)", pk, type(pk))
        return InuitsNonMemberSerializer().to_representation(InuitsNonMember.objects.get(pk=str(pk)))
