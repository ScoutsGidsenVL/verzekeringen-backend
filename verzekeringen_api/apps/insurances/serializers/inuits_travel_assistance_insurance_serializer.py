import logging

from apps.equipment.serializers import InuitsVehicleSerializer
from apps.people.serializers import InuitsNonMemberSerializer

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.serializers import TravelAssistanceInsuranceSerializer


logger = logging.getLogger(__name__)


class InuitsTravelAssistanceInsuranceSerializer(TravelAssistanceInsuranceSerializer):
    participants = InuitsNonMemberSerializer(many=True)
    # vehicle = serializers.SerializerMethodField(required=False)
    vehicle = InuitsVehicleSerializer()

    class Meta:
        model = TravelAssistanceInsurance
        fields = TravelAssistanceInsuranceSerializer.Meta.fields

    # @swagger_serializer_method(serializer_or_field=InuitsVehicleSerializer)
    # def get_vehicle(self, obj):
    #     logger.debug("VEHICLE OBJ: %s", obj)
    #     vehicle = obj.vehicle

    #     if vehicle:

    #         inuits_vehicles = InuitsVehicle.objects.filter(
    #             Q(brand=vehicle.brand) | Q(license_plate=vehicle.license_plate)
    #         )

    #         if inuits_vehicles.count() > 0:
    #             return InuitsVehicleSerializer(inuits_vehicles[0]).data

    #         return InuitsVehicleSerializer(vehicle).data

    #     return None
