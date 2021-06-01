from django.urls import path
from rest_framework import routers
from .api.views import BelgianPostcodeCitySearch, InuitsNonMemberViewSet

router = routers.SimpleRouter()
router.register(r"non_member", InuitsNonMemberViewSet, "InuitsNonMember")

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("belgian_city_search/", BelgianPostcodeCitySearch.as_view()),
    ]
)
