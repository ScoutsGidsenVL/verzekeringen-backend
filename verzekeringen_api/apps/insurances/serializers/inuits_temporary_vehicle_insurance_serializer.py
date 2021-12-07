from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.serializers import TemporaryVehicleInsuranceSerializer


class InuitsTemporaryVehicleInsuranceSerializer(TemporaryVehicleInsuranceSerializer):
    class Meta:
        model = TemporaryVehicleInsurance
        fields = TemporaryVehicleInsuranceSerializer.Meta.fields
