from rest_framework import routers
from apps.insurances.api.views import (
    InsuranceClaimViewSet,
    InsuranceClaimAttachmentViewSet,
    InsuranceTypeViewSet,
    InsuranceViewSet,
    InsuranceStatusViewSet,
    InsuranceDraftViewSet,
    GroupSizeViewSet,
    EventSizeViewSet,
    TemporaryVehicleInsuranceCoverageOptionViewSet,
    TemporaryVehicleInsuranceOptionApiViewSet,
    EventInsuranceAttachmentViewSet,
    ActivityInsuranceAttachmentViewSet,
)

router = routers.SimpleRouter()
router.register(r"insurance_types", InsuranceTypeViewSet, "InsuranceType")
router.register(r"insurances", InsuranceViewSet, "Insurance")
router.register(r"insurances_claims", InsuranceClaimViewSet, "Insurance Claims")
router.register(r"insurance_drafts", InsuranceDraftViewSet, "InsuranceDraft")
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
    TemporaryVehicleInsuranceOptionApiViewSet,
    "VehicleInsuranceOption",
)
router.register(r"files", InsuranceClaimAttachmentViewSet, "Files")
router.register(r"events/participants", EventInsuranceAttachmentViewSet, "EventInsuranceFiles")
router.register(r"activities/participants", ActivityInsuranceAttachmentViewSet, "ActivityInsuranceFiles")


urlpatterns = router.urls
