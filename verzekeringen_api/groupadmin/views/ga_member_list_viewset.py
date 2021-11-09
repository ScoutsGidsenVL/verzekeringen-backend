import requests

from django.http import Http404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from groupadmin.serializers import ScoutsMemberDetailSerializer, ScoutsMemberListSerializer
from groupadmin.services import GroupAdmin


class ScoutsMemberListView(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    service = GroupAdmin()

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberDetailSerializer})
    def view_member_list_member_detail(self, request, **kwargs):
        group_admin_id = kwargs.get("id")

        try:
            result = self.service.group_admin_member_detail(active_user=request.user, group_admin_id=group_admin_id)
        except requests.exceptions.HTTPError as error:
            if error.response.status_code == 404:
                raise Http404
            raise error
        output_serializer = ScoutsMemberDetailSerializer(result)

        return Response(output_serializer.data)
