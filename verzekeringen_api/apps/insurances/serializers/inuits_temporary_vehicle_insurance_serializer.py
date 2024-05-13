from apps.people.serializers import InuitsNonMemberSerializer
from scouts_insurances.insurances.models import TemporaryVehicleInsurance
from scouts_insurances.insurances.serializers import TemporaryVehicleInsuranceSerializer


class InuitsTemporaryVehicleInsuranceSerializer(TemporaryVehicleInsuranceSerializer):
    owner = InuitsNonMemberSerializer()
    drivers = InuitsNonMemberSerializer(many=True)

    class Meta:
        model = TemporaryVehicleInsurance
        fields = TemporaryVehicleInsuranceSerializer.Meta.fields
