from django.urls import path
from django.conf.urls import include


urlpatterns = [
    path("", include("scouts_insurances.equipment.urls")),
    path("", include("scouts_insurances.info.urls")),
    path("", include("scouts_insurances.insurances.urls")),
    path("", include("scouts_insurances.locations.urls")),
]
