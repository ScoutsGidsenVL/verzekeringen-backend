from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path("", include("scouts_insurances.equipment.urls")),
    path("", include("scouts_insurances.info.urls")),
    path("", include("scouts_insurances.locations.urls")),
]
