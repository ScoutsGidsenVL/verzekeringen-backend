from django.urls import path, include
from rest_framework import routers
from .api.views import VehicleTypeViewSet, VehicleViewSet, VehicleTrailerOptionViewSet, InuitsEquipmentViewSet

router = routers.SimpleRouter()
router.register(r"vehicle_types", VehicleTypeViewSet, "VehicleType")
router.register(r"vehicle_trailer_options", VehicleTrailerOptionViewSet, "VehicleTrailerOption")
router.register(r"vehicles", VehicleViewSet, "Vehicle")
router.register(r"equipment", InuitsEquipmentViewSet, "Equipment")

urlpatterns = router.urls
