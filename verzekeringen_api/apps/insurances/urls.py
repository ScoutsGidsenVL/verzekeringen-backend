from django.urls import path, include
from rest_framework import routers
from .api.views import (
    InsuranceTypeViewSet,
    InsuranceViewSet,
    InsuranceStatusViewSet,
    InsuranceDraftViewSet,
    GroupSizeViewSet,
    EventSizeViewSet,
    TemporaryVehicleInsuranceCoverageOptionViewSet,
    TemporaryVehicleInsuranceOptionApiViewSet,
)

router = routers.SimpleRouter()
router.register(r"insurance_types", InsuranceTypeViewSet, "InsuranceType")
router.register(r"insurances", InsuranceViewSet, "Insurance")
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


urlpatterns = router.urls
