import logging
from typing import List
from datetime import datetime
import uuid

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.people.models import InuitsNonMember
from apps.people.filters import InuitsNonMemberFilter
from apps.people.serializers import PersonSerializer

from scouts_insurances.people.models import NonMember
from scouts_insurances.insurances.models.enums import InsuranceTypeEnum

from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.inuits.utils import DateUtils
from apps.utils.utils import AuthenticationHelper


logger = logging.getLogger(__name__)


class PersonSearch(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsNonMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]
    service = GroupAdminMemberService()

    def get_queryset(self):
        group = self.request.query_params.get("group")
        return InuitsNonMember.objects.filter(group_admin_id=group).allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: PersonSerializer})
    def list(self, request):
        return self._list(request=request)

    @swagger_auto_schema(
        responses={status.HTTP_200_OK: PersonSerializer},
    )
    @action(methods=["get"], detail=False, url_path="/inactive")
    def list_with_previous_members(self, request):
        return self._list(request=request, include_inactive=True)

    def _list(self, request, include_inactive: bool = False):
        search_term = self.request.GET.get("term", None)
        group_group_admin_id = self.request.GET.get("group", None)
        AuthenticationHelper.has_rights_for_group(request.user, group_group_admin_id)
        start = DateUtils.datetime_from_isoformat(self.request.GET.get("start", None))
        end = DateUtils.datetime_from_isoformat(self.request.GET.get("end", None))
        type = InsuranceTypeEnum.parse_type(self.request.GET.get("type", None))

        if not search_term:
            raise ValidationError("Url param 'term' is a required filter")

        if not group_group_admin_id:
            logger.debug("Searching for members and non-members with search term %s", search_term)
        else:
            logger.debug("Searching for members and non-members with term and group %s", group_group_admin_id)

        if start and end:
            logger.debug("Searching for non-members who are already insured between %s and %s", start, end)

        members: List[AbstractScoutsMember] = self.service.search_member_filtered(
            active_user=request.user, term=search_term, group_group_admin_id=group_group_admin_id
        )

        # Include non-members with a running insurance in the search results if needed
        queryset = self.get_queryset()
        inuits_non_members = self.filter_queryset(queryset)
        if type and inuits_non_members and start and end:
            if type is InsuranceTypeEnum.EQUIPMENT:
                pass
            elif type is InsuranceTypeEnum.TEMPORARY:
                pass
            elif type is InsuranceTypeEnum.TEMPORARY_VEHICLE:
                pass
            elif (
                type is InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE
                or InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE
            ):
                pass

            inuits_non_members = NonMember.objects.get_queryset().currently_insured(
                start, end, [str(inuits_non_member.id) for inuits_non_member in inuits_non_members], type
            )
        results = [*members, *inuits_non_members]
        output_serializer = PersonSerializer(results, many=True)

        return Response(output_serializer.data)
