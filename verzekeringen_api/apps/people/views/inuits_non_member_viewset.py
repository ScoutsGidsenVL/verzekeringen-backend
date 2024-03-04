import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from apps.people.serializers import InuitsNonMemberSerializer
from apps.people.filters import InuitsNonMemberFilter
from apps.people.services import InuitsNonMemberService
from apps.people.models import InuitsNonMember
from apps.utils.utils import AuthenticationHelper

from scouts_insurances.insurances.models.enums import InsuranceTypeEnum

from scouts_auth.inuits.utils import DateUtils


logger = logging.getLogger(__name__)


class InuitsNonMemberViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsNonMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = InuitsNonMemberService()

    def get_queryset(self):
        group = self.request.query_params.get('group')

        return InuitsNonMember.objects.filter(group_admin_id=group)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsNonMemberSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InuitsNonMemberSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsNonMemberSerializer})
    def list(self, request):
        group = self.request.query_params.get('group')
        type = int(self.request.query_params.get('type', 0))
        start = DateUtils.datetime_from_isoformat(
            self.request.query_params.get('start', None))
        end = DateUtils.datetime_from_isoformat(
            self.request.query_params.get('end', None))

        AuthenticationHelper.has_rights_for_group(request.user, group)

        inuits_non_members = self.filter_queryset(self.get_queryset())
        if not type is int(InsuranceTypeEnum.TEMPORARY):
            inuits_non_members = InuitsNonMember.objects.get_queryset().not_currently_temporarily_insured(
                request.user, start, end, inuits_non_members)

        page = self.paginate_queryset(inuits_non_members)

        if page is not None:
            serializer = InuitsNonMemberSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsNonMemberSerializer(
                inuits_non_members, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsNonMemberSerializer,
        responses={status.HTTP_201_CREATED: InuitsNonMemberSerializer},
    )
    def create(self, request):
        logger.debug("REQUEST DATA: %s", request.data)
        group = request.data["group_admin_id"]
        AuthenticationHelper.has_rights_for_group(request.user, group)
        input_serializer = InuitsNonMemberSerializer(
            data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("VALIDATED REQUEST DATA: %s", validated_data)

        non_member = self.service.inuits_non_member_create(
            inuits_non_member=validated_data, created_by=request.user)

        output_serializer = InuitsNonMemberSerializer(
            non_member, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsNonMemberSerializer,
        responses={status.HTTP_200_OK: InuitsNonMemberSerializer},
    )
    def partial_update(self, request, pk=None):
        inuits_non_member = InuitsNonMember.objects.get(
            id=request.data.get('inuits_id'))

        serializer = InuitsNonMemberSerializer(
            instance=inuits_non_member, data=request.data, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        inuits_non_member = self.service.inuits_non_member_update(
            inuits_non_member=inuits_non_member,
            updated_inuits_non_member=serializer.validated_data,
            updated_by=request.user,
        )

        output_serializer = InuitsNonMemberSerializer(inuits_non_member)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
