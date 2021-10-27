import requests
from django.urls import path, include
from rest_framework import routers

from scouts_auth.apps import ScoutsAuthConfig
from scouts_auth.views import (
    CurrentUserView,
    OIDCAuthCodeView,
    OIDCRefreshView,
    GroupAdminFunctionView,
    GroupAdminGroupView,
    GroupAdminMemberListView,
    GroupAdminMemberMedicalFlashCardView,
    GroupAdminMemberView,
    GroupAdminPartialMemberView,
)


# router = routers.SimpleRouter()
# router.register(r"^ga/functions/", GroupAdminFunctionView, "ga_functions")
# router.register(r"^ga/groups/", GroupAdminGroupView, "ga_groups")
# router.register(r"^ga/members/", GroupAdminMemberListMemberView, "ga_member_list")
# router.register(r"^ga/flash_card/", GroupAdminMemberMedicalFlashCardView, "ga_medical_flash_card")
# router.register(r"^ga/member/", GroupAdminMemberView, "ga_member")
# router.register(r"^ga/search/", GroupAdminPartialMemberView, "ga_member_search")

# urlpatterns = [
#     path("ga/", GroupAdminView.as_view(), name="groupadmin"),
#     # The infamous "me" call
#     path("auth/me/", CurrentUserView.as_view(), name="me"),
#     # Authenticate with OIDC
#     path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
#     # Refresh the OIDC authentication
#     path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
#     # Needed for route cascading
#     path("oidc/", include("mozilla_django_oidc.urls")),
# ]

urlpatterns = [
    path("ga/members/list/", GroupAdminMemberListView.as_view(), name="ga_member_list"),
    path("ga/groups/", GroupAdminGroupView.as_view(), name="ga_groups"),
    # The infamous "me" call
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    # Authenticate with OIDC
    path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
    # Refresh the OIDC authentication
    path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
    # path("oidc/", include("mozilla_django_oidc.urls")),
]
# urlpatterns += router.urls
