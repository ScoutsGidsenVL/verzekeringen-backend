from django.urls import path, include
from rest_framework import routers
from .api.views import VehicleTypeViewSet, VehicleViewSet

router = routers.SimpleRouter()
router.register(r"vehicle_types", VehicleTypeViewSet, "VehicleType")
router.register(r"vehicles", VehicleViewSet, "Vehicle")

urlpatterns = router.urls
