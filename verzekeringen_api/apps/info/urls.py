from rest_framework import routers

from apps.info.api.views import InfoVariableViewSet

router = routers.SimpleRouter()
router.register(r"info", InfoVariableViewSet, "InfoVariable")


urlpatterns = router.urls
