import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.people.serializers import InuitsNonMemberSerializer
from apps.people.filters import InuitsNonMemberFilter
from apps.people.services import InuitsNonMemberService
from apps.people.models import InuitsNonMember


logger = logging.getLogger(__name__)


class InuitsNonMemberViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsNonMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    service = InuitsNonMemberService()

    def get_queryset(self):
        return InuitsNonMember.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsNonMemberSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InuitsNonMemberSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsNonMemberSerializer})
    def list(self, request):
        non_members = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(non_members)

        if page is not None:
            serializer = InuitsNonMemberSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsNonMemberSerializer(non_members, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsNonMemberSerializer,
        responses={status.HTTP_201_CREATED: InuitsNonMemberSerializer},
    )
    def create(self, request):
        logger.debug("REQUEST DATA: %s", request.data)
        input_serializer = InuitsNonMemberSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        logger.debug("VALIDATED REQUEST DATA: %s", validated_data)

        created_non_member = self.service.inuits_non_member_create(**validated_data)

        output_serializer = InuitsNonMemberSerializer(created_non_member, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsNonMemberSerializer,
        responses={status.HTTP_200_OK: InuitsNonMemberSerializer},
    )
    def partial_update(self, request, pk=None):
        non_member = self.get_object()

        serializer = InuitsNonMemberSerializer(
            data=request.data, instance=non_member, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_non_member = self.service.inuits_non_member_update(non_member=non_member, **serializer.validated_data)

        output_serializer = InuitsNonMemberSerializer(updated_non_member)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
