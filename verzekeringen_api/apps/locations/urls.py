from django.urls import path
from rest_framework import routers

from apps.locations.api.views import BelgianPostcodeCitySearch, CountryViewSet

router = routers.SimpleRouter()
router.register(r"", CountryViewSet, "Country")

urlpatterns = router.urls
urlpatterns.extend(
    [
        path("belgian_city_search/", BelgianPostcodeCitySearch.as_view()),
    ]
)
