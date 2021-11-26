from rest_framework import serializers

from apps.equipment.models import InuitsEquipmentTemplate
from apps.equipment.serializers import InuitsEquipmentSerializer

from inuits.mixins import FlattenSerializerMixin


class InuitsEquipmentTemplateSerializer(FlattenSerializerMixin, serializers.Serializer):
    """Provides a bridge between Equipment and InuitsEquipment."""

    # The Equipment instance id, if any
    id = serializers.SerializerMethodField()

    class Meta:
        model = InuitsEquipmentTemplate
        fields = ["id", "inuits_equipment"]
        # The InuitsEquipment to create/read/update/delete
        flatten = [("inuits_equipment", InuitsEquipmentSerializer())]

    def get_id(self, obj: InuitsEquipmentTemplate):
        try:
            return obj.id
        except:
            return None
