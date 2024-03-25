from rest_framework import serializers

from apps.equipment.models import InuitsEquipmentTemplate
from apps.equipment.serializers import InuitsEquipmentSerializer
from scouts_auth.inuits.mixins import FlattenSerializerMixin


class InuitsEquipmentTemplateSerializer(FlattenSerializerMixin, serializers.Serializer):
    """Provides a bridge between Equipment and InuitsEquipment."""

    class Meta:
        model = InuitsEquipmentTemplate
        # fields = ["id", "inuits_equipment"]
        # The InuitsEquipment to create/read/update/delete
        exclude = ["created_on", "created_by", "updated_on", "updated_by"]
        flatten = [("inuits_equipment", InuitsEquipmentSerializer)]
