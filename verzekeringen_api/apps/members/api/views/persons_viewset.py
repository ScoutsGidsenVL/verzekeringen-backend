import logging
from datetime import date, datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.members.models import InuitsNonMember
from apps.members.api.filters import InuitsNonMemberFilter
from apps.members.api.serializers import PersonSerializer

from groupadmin.models import ScoutsMemberSearchResponse
from groupadmin.services import GroupAdminMemberService


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

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersonSerializer})
    def list(self, request):
        return self._list(request=request)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: PersonSerializer},
    )
    @action(methods=["get"], detail=False, url_path="/inactive")
    def list_with_previous_members(self, request):
        return self._list(request=request, include_inactive=True)

    def _list(self, request):
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)
        start = self.request.GET.get("start", None)
        end = self.request.GET.get("end", None)

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        if not group_group_admin_id:
            logger.debug("Searching for members and non-members with search term %s", search_term)
        else:
            logger.debug("Searching for members and non-members with term and group %s", group_group_admin_id)

        if start and end:
            logger.debug("Searching for non-members who are already insured between %s and %s", start, end)

        members: ScoutsMemberSearchResponse = self.service.search_member_filtered(
            active_user=request.user, term=search_term, group_group_admin_id=group_group_admin_id
        )

        queryset = self.get_queryset().with_group(group_group_admin_id)
        # Include non-members with a running insurance in the search results if needed
        if start and end:
            queryset = queryset.currently_insured(start, end)
        non_members = self.filter_queryset(queryset)
        results = [*members, *non_members]
        output_serializer = PersonSerializer(results, many=True)

        return Response(output_serializer.data)
