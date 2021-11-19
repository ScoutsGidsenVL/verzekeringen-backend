import logging
from datetime import date, datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.members.api.filters import InuitsNonMemberFilter
from apps.members.models import InuitsNonMember

from groupadmin.models import ScoutsMemberSearchResponse
from groupadmin.services import GroupAdminMemberService
from groupadmin.serializers import ScoutsMemberSearchFrontendSerializer


logger = logging.getLogger(__name__)


class PersonSearch(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsNonMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]
    service = GroupAdminMemberService()

    def get_queryset(self):
        return InuitsNonMember.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: ScoutsMemberSearchFrontendSerializer})
    def list(self, request):
        return self._list(request=request)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: ScoutsMemberSearchFrontendSerializer},
    )
    @action(methods=["get"], detail=False, url_path="/inactive")
    def list_with_previous_members(self, request):
        return self._list(request=request, include_inactive=True)

    def _list(self, request, include_inactive: bool = False):
        search_term = self.request.GET.get("term", None)
        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        logger.debug("Searching for member with search term %s", search_term)

        members: ScoutsMemberSearchResponse = self.service.search_member_filtered(
            active_user=request.user, term=search_term
        )
        non_members = self.filter_queryset(self.get_queryset())
        results = [*members, *non_members]
        output_serializer = ScoutsMemberSearchFrontendSerializer(results, many=True)

        return Response(output_serializer.data)
