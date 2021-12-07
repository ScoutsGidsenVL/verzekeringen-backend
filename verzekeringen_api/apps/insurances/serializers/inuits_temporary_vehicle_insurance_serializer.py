from apps.equipment.serializers import InuitsVehicleSerializer

from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.serializers import TemporaryVehicleInsuranceSerializer


class InuitsTemporaryVehicleInsuranceSerializer(TemporaryVehicleInsuranceSerializer):

    vehicle = InuitsVehicleSerializer()

    class Meta:
        model = TemporaryVehicleInsurance
        fields = TemporaryVehicleInsuranceSerializer.Meta.fields + ["vehicle"]
