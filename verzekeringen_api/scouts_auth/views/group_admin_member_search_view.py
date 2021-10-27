from rest_framework.exceptions import ValidationError
from rest_framework import views, status
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from scouts_auth.serializers import GroupAdminMemberListSerializer
from scouts_auth.services import GroupAdminMemberService


class GroupAdminMemberSearchView(views.APIView):

    service = GroupAdminMemberService()

    @swagger_auto_schema(responses={status.HTTP_200_OK: GroupAdminMemberListSerializer})
    def get(self, request):
        search_term = self.request.GET.get("term", None)
        group = self.request.GET.get("group", None)

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        results = self.service.group_admin_member_search(
            active_user=request.user, term=search_term, group=group
        )
        output_serializer = GroupAdminMemberListSerializer(results, many=True)

        return Response(output_serializer.data)
