from apps.equipment.serializers import InuitsEquipmentTemplateSerializer

from scouts_insurances.insurances.models import EquipmentInsurance
from scouts_insurances.insurances.serializers import EquipmentInsuranceSerializer


class InuitsEquipmentInsuranceSerializer(EquipmentInsuranceSerializer):
    # equipment = InuitsEquipmentTemplateSerializer(many=True)

    class Meta:
        model = EquipmentInsurance
        fields = EquipmentInsuranceSerializer.Meta.fields
