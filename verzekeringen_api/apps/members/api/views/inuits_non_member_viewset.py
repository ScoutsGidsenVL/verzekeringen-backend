from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import InuitsNonMemberOutputSerializer, InuitsNonMemberCreateInputSerializer
from ..filters import InuitsNonMemberFilter
from ...services import InuitsMemberService
from ...models import InuitsNonMember


class InuitsNonMemberViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = InuitsNonMemberFilter
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return InuitsNonMember.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsNonMemberOutputSerializer})
    def retrieve(self, request, pk=None):
        type = self.get_object()
        serializer = InuitsNonMemberOutputSerializer(type)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InuitsNonMemberOutputSerializer})
    def list(self, request):
        non_members = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(non_members)

        if page is not None:
            serializer = InuitsNonMemberOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InuitsNonMemberOutputSerializer(non_members, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InuitsNonMemberCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InuitsNonMemberOutputSerializer},
    )
    def create(self, request):
        input_serializer = InuitsNonMemberCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_non_member = InuitsMemberService.inuits_non_member_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InuitsNonMemberOutputSerializer(created_non_member, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=InuitsNonMemberCreateInputSerializer,
        responses={status.HTTP_200_OK: InuitsNonMemberOutputSerializer},
    )
    def partial_update(self, request, pk=None):
        non_member = self.get_object()

        serializer = InuitsNonMemberCreateInputSerializer(
            data=request.data, instance=non_member, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_non_member = InuitsMemberService.inuits_non_member_update(
            non_member=non_member, **serializer.validated_data
        )

        output_serializer = InuitsNonMemberOutputSerializer(updated_non_member)

        return Response(output_serializer.data, status=status.HTTP_200_OK)
