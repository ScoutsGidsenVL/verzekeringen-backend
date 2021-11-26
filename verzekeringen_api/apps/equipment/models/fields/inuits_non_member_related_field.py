from rest_framework import serializers

from apps.people.models import InuitsNonMember

# Special filter field so we can get allowed in queryset
class InuitsEquipmentNonMemberRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get("request", None)
        queryset = InuitsNonMember.objects.all().allowed(request.user)
        return queryset
