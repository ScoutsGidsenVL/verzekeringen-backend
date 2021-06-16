from django.urls import path, include
from rest_framework import routers
from .api.views import InfoVariableViewSet

router = routers.SimpleRouter()
router.register(r"info", InfoVariableViewSet, "InfoVariable")


urlpatterns = router.urls
