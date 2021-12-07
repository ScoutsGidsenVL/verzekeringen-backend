from rest_framework import routers
from scouts_insurances.insurances.views import (
    InsuranceTypeViewSet,
    InsuranceStatusViewSet,
    GroupSizeViewSet,
    EventSizeViewSet,
    TemporaryVehicleInsuranceCoverageOptionViewSet,
    TemporaryVehicleInsuranceOptionViewSet,
    BaseInsuranceViewSet,
    EquipmentInsuranceViewSet,
    TemporaryInsuranceViewSet,
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
router.register(r"insurances/equipment", EquipmentInsuranceViewSet, "EquipmentInsurance")
router.register(r"insurances/temporary", TemporaryInsuranceViewSet, "TemporaryInsurance")
router.register(r"insurances", BaseInsuranceViewSet, "Insurance")


urlpatterns = router.urls
