from django.urls import path
from .views import FileViewSet
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"files", FileViewSet, "Files")

urlpatterns = router.urls
