from .event_insurance_attachment_serializers import (
    EventInsuranceAttachmentSerializer,
    EventInsuranceAttachmentUploadSerializer,
)
from .activity_insurance_attachment_serializers import (
    ActivityInsuranceAttachmentSerializer,
    ActivityInsuranceAttachmentUploadSerializer,
)
from .insurance_draft_serializers import InsuranceDraftSerializer
from .insurance_claim_attachment_serializers import (
    InsuranceClaimAttachmentSerializer,
    InsuranceClaimAttachmentUploadSerializer,
)
from .insurance_claim_serializers import (
    InsuranceClaimCreateDataSerializer,
    InuitsClaimVictimSerializer,
    InsuranceClaimSerializer,
)
from .inuits_event_insurance_serializer import InuitsEventInsuranceSerializer
from .inuits_activity_insurance_serializer import InuitsActivityInsuranceSerializer
from .inuits_temporary_insurance_serializer import InuitsTemporaryInsuranceSerializer
from .inuits_temporary_vehicle_insurance_serializer import InuitsTemporaryVehicleInsuranceSerializer
from .inuits_travel_assistance_insurance_serializer import InuitsTravelAssistanceInsuranceSerializer
from .inuits_equipment_insurance_serializer import InuitsEquipmentInsuranceSerializer
