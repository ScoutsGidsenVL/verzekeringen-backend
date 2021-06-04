from django.urls import path
from .api.views import BelgianPostcodeCitySearch, CountryByInsuranceTypeView

urlpatterns = [
    path("belgian_city_search/", BelgianPostcodeCitySearch.as_view()),
    path("countries_by_type/<int:type_id>", CountryByInsuranceTypeView.as_view()),
]
