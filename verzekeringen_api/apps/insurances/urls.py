from rest_framework import routers

from apps.insurances.views import (
    InsuranceTypeViewSet,
    InsuranceStatusViewSet,
    GroupSizeViewSet,
    EventSizeViewSet,
    TemporaryVehicleInsuranceCoverageOptionViewSet,
    TemporaryVehicleInsuranceOptionViewSet,
    BaseInsuranceViewSet,
    TemporaryInsuranceViewSet,
    InsuranceClaimViewSet,
    InsuranceClaimAttachmentViewSet,
    InsuranceDraftViewSet,
    ActivityInsuranceAttachmentViewSet,
    EventInsuranceAttachmentViewSet,
    InuitsEventInsuranceViewSet,
    InuitsActivityInsuranceViewSet,
    InuitsTemporaryVehicleInsuranceViewSet,
    InuitsTravelAssistanceInsuranceViewSet,
    InuitsEquipmentInsuranceViewSet,
)

router = routers.SimpleRouter()

router.register(r"insurance_types", InsuranceTypeViewSet, "InsuranceType")
router.register(r"insurance_statuses", InsuranceStatusViewSet, "InsuranceStatus")
router.register(r"insurance_group_sizes", GroupSizeViewSet, "GroupSize")
router.register(r"insurance_event_sizes", EventSizeViewSet, "EventSize")
router.register(
    r"vehicle_insurance_coverage_options",
    TemporaryVehicleInsuranceCoverageOptionViewSet,
    "VehicleInsuranceCoverageOption",
)
router.register(
    r"vehicle_insurance_options",
    TemporaryVehicleInsuranceOptionViewSet,
    "VehicleInsuranceOption",
)
router.register(r"insurances/temporary", TemporaryInsuranceViewSet, "TemporaryInsurance")

router.register(r"insurances/event", InuitsEventInsuranceViewSet, "EventInsurance")
router.register(r"insurances/activity", InuitsActivityInsuranceViewSet, "ActivityInsurance")
router.register(r"insurances/temporary_vehicle", InuitsTemporaryVehicleInsuranceViewSet, "TemporaryVehicleInsurance")
router.register(r"insurances/travel_assistance", InuitsTravelAssistanceInsuranceViewSet, "TravelAssistanceInsurance")
router.register(r"insurances_claims", InsuranceClaimViewSet, "Insurance Claims")
router.register(r"insurance_drafts", InsuranceDraftViewSet, "InsuranceDraft")
router.register(r"files", InsuranceClaimAttachmentViewSet, "Files")
router.register(r"activities/participants", ActivityInsuranceAttachmentViewSet, "ActivityInsuranceFiles")
router.register(r"events/participants", EventInsuranceAttachmentViewSet, "EventInsuranceFiles")
router.register(r"insurances/equipment", InuitsEquipmentInsuranceViewSet, "EquipmentInsurance")
router.register(r"insurances", BaseInsuranceViewSet, "Insurance")


urlpatterns = router.urls
