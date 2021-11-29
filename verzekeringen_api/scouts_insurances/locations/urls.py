from django.urls import path
from rest_framework import routers

from scouts_insurances.locations.views import CountryViewSet, BelgianPostalCodeCitySearch

router = routers.SimpleRouter()
router.register(r"", CountryViewSet, "Country")

urlpatterns = router.urls
urlpatterns.extend(
    [
        path("belgian_city_search/", BelgianPostalCodeCitySearch.as_view()),
    ]
)
