import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, permissions, status, viewsets
from rest_framework.response import Response

from apps.insurances.models import InsuranceDraft
from apps.insurances.serializers import InsuranceDraftSerializer
from apps.insurances.services import InsuranceDraftService
from apps.utils.utils import AuthenticationHelper

logger = logging.getLogger(__name__)


class InsuranceDraftViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]
    service = InsuranceDraftService()

    def get_queryset(self):
        return InsuranceDraft.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=InsuranceDraftSerializer,
        responses={status.HTTP_201_CREATED: InsuranceDraftSerializer},
    )
    def create(self, request):
        group = self.request.data["data"]["scouts_group"]["group_admin_id"]
        AuthenticationHelper.has_rights_for_group(request.user, group)
        input_serializer = InsuranceDraftSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data
        draft = self.service.insurance_draft_create(**validated_data, created_by=request.user)

        output_serializer = InsuranceDraftSerializer(draft)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceDraftSerializer})
    def retrieve(self, request, pk=None):
        draft = self.get_object()
        serializer = InsuranceDraftSerializer(draft)

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InsuranceDraftSerializer,
        responses={status.HTTP_201_CREATED: InsuranceDraftSerializer},
    )
    def partial_update(self, request, pk=None):
        draft = self.get_object()
        input_serializer = InsuranceDraftSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)
        new_draft = self.service.insurance_draft_update(
            draft=draft, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceDraftSerializer(new_draft)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        draft = self.get_object()
        group = draft.data["scouts_group"]["group_admin_id"]
        AuthenticationHelper.has_rights_for_group(request.user, group)
        self.service.insurance_draft_delete(draft=draft)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceDraftSerializer})
    def list(self, request):
        drafts = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(drafts)

        if page is not None:
            serializer = InsuranceDraftSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InsuranceDraftSerializer(drafts, many=True)
            return Response(serializer.data)
