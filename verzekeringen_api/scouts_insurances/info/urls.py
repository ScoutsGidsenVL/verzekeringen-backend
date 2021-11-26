from rest_framework import routers

from scouts_insurances.info.views import InfoVariableViewSet

router = routers.SimpleRouter()
router.register(r"info", InfoVariableViewSet, "InfoVariable")


urlpatterns = router.urls
