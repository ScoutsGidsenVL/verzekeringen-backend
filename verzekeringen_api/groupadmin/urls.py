from django.urls import path

from groupadmin.views import (
    ScoutsAllowedCallsView,
    ScoutsFunctionView,
    ScoutsGroupView,
    ScoutsMemberView,
    ScoutsMemberListView,
)

view_allowed_calls = ScoutsAllowedCallsView.as_view({"get": "view_allowed_calls"})
view_member_profile = ScoutsMemberView.as_view({"get": "view_member_profile"})
view_member_list = ScoutsMemberView.as_view({"get": "view_member_list"})
view_search_members = ScoutsMemberView.as_view({"get": "search_members"})
view_member = ScoutsMemberView.as_view({"get": "view_member_info"})
view_group_list = ScoutsGroupView.as_view({"get": "view_groups"})
view_accountable_group_list = ScoutsGroupView.as_view({"get": "view_accountable_groups"})
view_group = ScoutsGroupView.as_view({"get": "view_group"})
view_function_list = ScoutsFunctionView.as_view({"get": "view_function_list"})
view_function = ScoutsFunctionView.as_view({"get": "view_function"})
view_member_list_members = ScoutsMemberListView.as_view({"get": "view_member_list_members"})
view_member_list_member_detail = ScoutsMemberListView.as_view({"get": "view_member_list_member_detail"})

urlpatterns = [
    path("ga/allowed_calls", view_allowed_calls, name="ga_allowed_calls"),
    path("ga/members/list/", view_member_list, name="ga_member_list"),
    path("ga/members/search/<str:term>/", view_search_members, name="ga_search_members"),
    path("ga/members/search/<str:term>/<str:group>/", view_search_members, name="ga_search_members_with_group"),
    path("ga/members/info/<str:group_admin_id>", view_member, name="ga_member"),
    path("ga/members/profile", view_member_profile, name="ga_member_profile"),
    path("ga/groups/", view_group_list, name="ga_groups"),
    path("ga/groups/accountable/", view_accountable_group_list, name="ga_groups"),
    path("ga/groups/<str:group_number>", view_group, name="ga_group"),
    path("ga/functions/group/<str:group_number_fragment>", view_function_list, name="ga_functions"),
    path("ga/functions/<str:function_id>", view_function, name="ga_function"),
]
