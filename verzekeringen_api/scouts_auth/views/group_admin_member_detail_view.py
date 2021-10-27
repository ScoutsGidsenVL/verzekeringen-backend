import requests

from django.http import Http404
from rest_framework import views, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.serializers import GroupAdminMemberDetailSerializer
from scouts_auth.services import GroupAdminMemberService


class GroupAdminMemberDetailView(views.APIView):

    service = GroupAdminMemberService()

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: GroupAdminMemberDetailSerializer}
    )
    def get(self, request, **kwargs):
        group_admin_id = kwargs.get("id")

        try:
            result = self.service.group_admin_member_detail(
                active_user=request.user, group_admin_id=group_admin_id
            )
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error
        output_serializer = GroupAdminMemberDetailSerializer(result)

        return Response(output_serializer.data)
