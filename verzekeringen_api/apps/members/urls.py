from django.urls import path
from rest_framework import routers
from .api.views import (
    InuitsNonMemberViewSet,
    GroupAdminMemberSearch,
    GroupAdminMemberDetail,
)

router = routers.SimpleRouter()
router.register(r"non_member", InuitsNonMemberViewSet, "InuitsNonMember")

urlpatterns = router.urls

urlpatterns.extend(
    [
        path("members_search/", GroupAdminMemberSearch.as_view()),
        path("members/<str:id>", GroupAdminMemberDetail.as_view()),
    ]
)
