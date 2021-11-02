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

view_member_list = GroupAdminMemberView.as_view({"get": "view_member_list"})
view_member = GroupAdminMemberView.as_view({"get": "view_member_info"})
view_group_list = GroupAdminGroupView.as_view({"get": "view_groups"})
view_accountable_group_list = GroupAdminGroupView.as_view({"get": "view_accountable_groups"})
view_group = GroupAdminGroupView.as_view({"get": "view_group"})
view_function_list = GroupAdminFunctionView.as_view({"get": "view_function_list"})

urlpatterns = [
    path("ga/members/list/", view_member_list, name="ga_member_list"),
    path("ga/member/<str:group_admin_id>", view_member, name="ga_member"),
    # path("ga/groups/", GroupAdminGroupListView.as_view(), name="ga_groups"),
    # path("ga/groups/accountable/", GroupAdminAccountableGroupListView.as_view(), name="ga_groups"),
    # path("ga/groups/<str:group_number>", GroupAdminGroupView.as_view(), name="ga_group"),
    path("ga/groups/", view_group_list, name="ga_groups"),
    path("ga/groups/accountable/", view_accountable_group_list, name="ga_groups"),
    path("ga/groups/<str:group_number>", view_group, name="ga_group"),
    path("ga/functions/<str:group_number_fragment>", view_function_list, name="ga_functions"),
    # The infamous "me" call
    path("auth/me/", CurrentUserView.as_view(), name="me"),
    # Authenticate with OIDC
    path("oidc/token/", OIDCAuthCodeView.as_view(), name="token"),
    # Refresh the OIDC authentication
    path("oidc/refresh/", OIDCRefreshView.as_view(), name="refresh"),
    # path("oidc/", include("mozilla_django_oidc.urls")),
]
# urlpatterns += router.urls
