from rest_framework import serializers

from apps.equipment.models import InuitsVehicleTemplate
from apps.equipment.serializers import InuitsVehicleSerializer

from scouts_auth.inuits.mixins import FlattenSerializerMixin


class InuitsVehicleTemplateSerializer(FlattenSerializerMixin, serializers.Serializer):
    """Provides a bridge between the vehicle data in TemporaryVehicleInsurance and InuitsVehicle."""

    # The TemporaryVehicleInsurance id
    id = serializers.SerializerMethodField()

    class Meta:
        model = InuitsVehicleTemplate
        fields = "id, inuits_vehicle"
        # The InuitsVehicle to create/read/update/delete
        flatten = [("inuits_vehicle", InuitsVehicleSerializer)]

    def get_id(self, obj: InuitsVehicleTemplate):
        try:
            return obj.temporary_vehicle_insurance.id
        except:
            return None
