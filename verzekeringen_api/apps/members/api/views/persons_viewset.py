from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import views, viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from ..filters import InuitsNonMemberFilter
from ..serializers import (
    GroupAdminMemberListOutputSerializer,
    GroupAdminMemberDetailOutputSerializer,
    PersonOutputSerializer,
)
from ...models import InuitsNonMember
from ...services import GroupAdminMemberService


class PersonSearch(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsNonMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return InuitsNonMember.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersonOutputSerializer})
    def list(self, request):
        return self._list(request=request)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: PersonOutputSerializer},
    )
    @action(methods=["get"], detail=False, url_path="/inactive")
    def list_with_previous_members(self, request):
        return self._list(request=request, include_inactive=True)

    def _list(self, request, include_inactive: bool = False):
        search_term = self.request.GET.get("term", None)
        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        members = GroupAdminMemberService.group_admin_member_search(
            active_user=request.user, term=search_term, include_inactive=include_inactive
        )
        non_members = self.filter_queryset(self.get_queryset())
        results = [*members, *non_members]
        output_serializer = PersonOutputSerializer(results, many=True)

        return Response(output_serializer.data)
