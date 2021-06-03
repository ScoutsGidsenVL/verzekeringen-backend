import requests
from django.http import Http404
from rest_framework import views, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import GroupAdminMemberListOutputSerializer, GroupAdminMemberDetailOutputSerializer
from ...services import GroupAdminMemberService
from ...utils import GroupAdminMember


class GroupAdminMemberSearch(views.APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberListOutputSerializer})
    def get(self, request):
        search_term = self.request.GET.get("term", None)
        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        results = GroupAdminMemberService.group_admin_member_search(active_user=request.user, term=search_term)
        output_serializer = GroupAdminMemberListOutputSerializer(results, many=True)

        return Response(output_serializer.data)


class GroupAdminMemberDetail(views.APIView):
    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberDetailOutputSerializer})
    def get(self, request, **kwargs):
        group_admin_id = kwargs.get("id")

        try:
            result = GroupAdminMemberService.group_admin_member_detail(
                active_user=request.user, group_admin_id=group_admin_id
            )
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error
        output_serializer = GroupAdminMemberDetailOutputSerializer(result)

        return Response(output_serializer.data)
