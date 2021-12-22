from apps.people.serializers import InuitsNonMemberSerializer

from scouts_insurances.insurances.models import TemporaryInsurance
from scouts_insurances.insurances.serializers import TemporaryInsuranceSerializer


class InuitsTemporaryInsuranceSerializer(TemporaryInsuranceSerializer):
    non_members = InuitsNonMemberSerializer(many=True)

    class Meta:
        model = TemporaryInsurance
        fields = TemporaryInsuranceSerializer.Meta.fields
