from rest_framework import routers
from apps.insurances.views import (
    InsuranceClaimViewSet,
    InsuranceClaimAttachmentViewSet,
    InsuranceDraftViewSet,
    ActivityInsuranceAttachmentViewSet,
    EventInsuranceAttachmentViewSet,
)

router = routers.SimpleRouter()
router.register(r"insurances_claims", InsuranceClaimViewSet, "Insurance Claims")
router.register(r"insurance_drafts", InsuranceDraftViewSet, "InsuranceDraft")
router.register(r"files", InsuranceClaimAttachmentViewSet, "Files")
router.register(r"activities/participants", ActivityInsuranceAttachmentViewSet, "ActivityInsuranceFiles")
router.register(r"events/participants", EventInsuranceAttachmentViewSet, "EventInsuranceFiles")


urlpatterns = router.urls
