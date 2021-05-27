from django.urls import path
from .api.views import BelgianPostcodeCitySearch

urlpatterns = [
    path("belgian_city_search/", BelgianPostcodeCitySearch.as_view()),
]
