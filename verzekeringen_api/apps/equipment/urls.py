from apps.equipment.views import InuitsEquipmentViewSet, InuitsVehicleViewSet
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"vehicles", InuitsVehicleViewSet, "InuitsVehicle")
router.register(r"equipment", InuitsEquipmentViewSet, "InuitsEquipment")

urlpatterns = router.urls
