from rest_framework import routers

from scouts_insurances.equipment.views import VehicleTrailerOptionViewSet, VehicleTypeViewSet

router = routers.SimpleRouter()

router.register(r"vehicle_trailer_options", VehicleTrailerOptionViewSet, "VehicleTrailerOption")
router.register(r"vehicle_types", VehicleTypeViewSet, "VehicleType")

urlpatterns = router.urls
