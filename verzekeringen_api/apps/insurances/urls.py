from django.urls import path, include
from rest_framework import routers
from .api.views import InsuranceTypeViewSet, InsuranceViewSet

router = routers.SimpleRouter()
router.register(r"insurance_types", InsuranceTypeViewSet, "InsuranceType")
router.register(r"insurances", InsuranceViewSet, "Insurance")

urlpatterns = router.urls
