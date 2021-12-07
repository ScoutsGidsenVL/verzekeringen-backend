from rest_framework import routers

from apps.insurances.views import (
    InsuranceClaimViewSet,
    InsuranceClaimAttachmentViewSet,
    InsuranceDraftViewSet,
    ActivityInsuranceAttachmentViewSet,
    EventInsuranceAttachmentViewSet,
    InuitsEventInsuranceViewSet,
    InuitsActivityInsuranceViewSet,
    InuitsTemporaryVehicleInsuranceViewSet,
    InuitsTravelAssistanceInsuranceViewSet,
)

router = routers.SimpleRouter()
router.register(r"insurances/event", InuitsEventInsuranceViewSet, "EventInsurance")
router.register(r"insurances/activity", InuitsActivityInsuranceViewSet, "ActivityInsurance")
router.register(r"insurances/temporary_vehicle", InuitsTemporaryVehicleInsuranceViewSet, "TemporaryVehicleInsurance")
router.register(r"insurances/travel_assistance", InuitsTravelAssistanceInsuranceViewSet, "TravelAssistanceInsurance")
router.register(r"insurances_claims", InsuranceClaimViewSet, "Insurance Claims")
router.register(r"insurance_drafts", InsuranceDraftViewSet, "InsuranceDraft")
router.register(r"files", InsuranceClaimAttachmentViewSet, "Files")
router.register(r"activities/participants", ActivityInsuranceAttachmentViewSet, "ActivityInsuranceFiles")
router.register(r"events/participants", EventInsuranceAttachmentViewSet, "EventInsuranceFiles")


urlpatterns = router.urls
