from django.urls import path, include
from rest_framework import routers
from .api.views import VehicleTypeViewSet

router = routers.SimpleRouter()
router.register(r"vehicle_types", VehicleTypeViewSet, "VehicleType")

urlpatterns = router.urls
