import logging
import uuid
from datetime import datetime
from typing import List

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.people.filters import InuitsNonMemberFilter
from apps.people.models import InuitsNonMember
from apps.people.serializers import PersonSerializer
from apps.utils.utils import AuthenticationHelper
from scouts_auth.groupadmin.models import AbstractScoutsMember
from scouts_auth.groupadmin.services import GroupAdminMemberService
from scouts_auth.inuits.utils import DateUtils
from scouts_insurances.insurances.models.enums import InsuranceTypeEnum
from scouts_insurances.people.models import NonMember

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

        logger.debug(
            f"Filtering people with params: term ({search_term}), group ({group_group_admin_id}), start ({start}), end ({end}), type ({type})"
        )

        members: List[AbstractScoutsMember] = self.service.search_member_filtered(
            active_user=request.user, term=search_term, group_group_admin_id=group_group_admin_id
        )

        # Include non-members with a running insurance in the search results if needed
        queryset = self.get_queryset()
        inuits_non_members = self.filter_queryset(queryset)
        logger.debug(f"Filtered inuits non-members: {len(inuits_non_members)} results")
        if type:
            if inuits_non_members and start and end:
                non_filtering_insurance_types = [
                    InsuranceTypeEnum.TEMPORARY_VEHICLE,
                    InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITH_VEHICLE_INSURANCE,
                    InsuranceTypeEnum.TRAVEL_ASSISTANCE_WITHOUT_VEHICLE_INSURANCE,
                ]
                if type in non_filtering_insurance_types:
                    logger.debug(f"Not filtering inuits non-members for {non_filtering_insurance_types}")
                    pass
                elif type is InsuranceTypeEnum.TEMPORARY:
                    inuits_non_members = InuitsNonMember.objects.get_queryset().not_currently_temporarily_insured(
                        request.user, start, end, inuits_non_members
                    )
                    logger.debug(
                        f"Filtered inuits non-members for {InsuranceTypEnum.TEMPORARY}: {len(inuits_non_members)} results"
                    )
                else:
                    inuits_non_members = InuitsNonMember.objects.get_queryset().currently_temporarily_insured(
                        request.user, start, end, inuits_non_members
                    )
                    logger.debug(
                        f"Filtered inuits non-members for all other insurance types: {len(inuits_non_members)} results"
                    )
        logger.debug("InuitsNonMember: %s", ",".join([person.last_name for person in inuits_non_members]))

        unique_non_members = []
        for inuits_non_member in inuits_non_members:
            result_appended = False
            for unique_non_member in unique_non_members:
                if (
                    inuits_non_member.last_name == unique_non_member.last_name
                    and (inuits_non_member.first_name == unique_non_member.first_name)
                    and (inuits_non_member.birth_date == unique_non_member.birth_date)
                ):
                    result_appended = True

            if not result_appended:
                unique_non_members.append(inuits_non_member)
        logger.debug("UNIQUE InuitsNonMember: %s", ",".join([person.last_name for person in unique_non_members]))

        results = [*members, *unique_non_members]
        output_serializer = PersonSerializer(results, many=True)

        return Response(output_serializer.data)
