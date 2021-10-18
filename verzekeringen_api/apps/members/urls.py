from django.urls import path
from rest_framework import routers

from apps.members.api.views import InuitsNonMemberViewSet

from scouts_auth.views import (
    GroupAdminMemberSearchView,
    GroupAdminMemberDetailView,
)
from .api.views.persons_viewset import PersonSearch

router = routers.SimpleRouter()
router.register(r"non_member", InuitsNonMemberViewSet, "InuitsNonMember")
router.register(r"persons", PersonSearch, "PersonSearch")

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("members_search/", GroupAdminMemberSearchView.as_view()),
        path("members/<str:id>", GroupAdminMemberDetailView.as_view()),
    ]
)
