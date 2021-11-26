from rest_framework import serializers

from scouts_insurances.people.serializers import NonMemberSerializer
from apps.locations.serializers import CountrySerializer

from scouts_insurances.insurances.models import TravelAssistanceInsurance
from scouts_insurances.insurances.serializers import BaseInsuranceFields, BaseInsuranceSerializer


class TravelAssistanceInsuranceSerializer(BaseInsuranceSerializer):
    participants = NonMemberSerializer(many=True)
    vehicle = serializers.SerializerMethodField()
    country = CountrySerializer()

    class Meta:
        model = TravelAssistanceInsurance
        fields = BaseInsuranceFields + ("country", "participants", "vehicle")

    # @swagger_serializer_method(serializer_or_field=InuitsVehicleOutputSerializer)
    # def get_vehicle(self, obj):
    #     vehicle = obj.vehicle

    #     if vehicle:

    #         inuits_vehicles = InuitsVehicle.objects.filter(
    #             Q(brand=vehicle.brand) | Q(license_plate=vehicle.license_plate)
    #         )

    #         if inuits_vehicles.count() > 0:
    #             return InuitsVehicleOutputSerializer(inuits_vehicles[0]).data

    #         return VehicleOutputSerializer(vehicle).data

    #     return None
    def validate_participants(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("At least one participant is required")
        return value
