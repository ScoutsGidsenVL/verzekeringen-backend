import logging

from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.datastructures import MultiValueDict
from rest_framework import viewsets, status, filters, parsers
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.api.serializers import (
    InsuranceClaimAttachmentUploadSerializer,
    BaseInsuranceClaimSerializer,
    InsuranceClaimInputSerializer,
    InsuranceClaimDetailOutputSerializer,
)
from apps.insurances.api.filters import InsuranceClaimFilter
from apps.insurances.models import InsuranceClaim
from apps.insurances.services import InsuranceClaimService
from inuits.utils import MultipartJsonParser


logger = logging.getLogger(__name__)


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    queryset = InsuranceClaim.objects.all()
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["victim__first_name", "victim__last_name", "group_number", "victim__group_admin_id"]
    ordering_fields = ["date"]
    ordering = ["-date"]

    # Filters on the year of the accident
    filterset_class = InsuranceClaimFilter
    service = InsuranceClaimService()

    serializer_class = InsuranceClaimInputSerializer
    parser_classes = [MultipartJsonParser, parsers.JSONParser]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # appending extra data to context
        if len(self.request.FILES) > 0:
            context.update({"attachments": self.request.FILES})

        return context

    @swagger_auto_schema(
        request_body=InsuranceClaimInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceClaimDetailOutputSerializer},
    )
    def create(self, request, *args, **kwargs):
        if len(request.FILES) != 1:
            raise ValidationError
        try:
            file_serializer = InsuranceClaimAttachmentUploadSerializer(data=request.FILES)
            file_serializer.is_valid(raise_exception=True)
        except Exception as exc:
            logger.error("Error while handling uploaded file", exc)
            raise ValidationError(
                message={"file": "Upload a valid file."},
                code=406,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        claim = self.get_object()
        serializer = InsuranceClaimDetailOutputSerializer(claim, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InsuranceClaimInputSerializer,
        responses={status.HTTP_200_OK: InsuranceClaimDetailOutputSerializer},
    )
    def partial_update(self, request, pk=None):
        claim = self.get_object()

        serializer = InsuranceClaimInputSerializer(
            data=request.data, instance=InsuranceClaim, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_claim = InsuranceClaimService.claim_update(claim=claim, **serializer.validated_data)

        output_serializer = InsuranceClaimDetailOutputSerializer(updated_claim, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceClaimSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        if page is not None:
            serializer = BaseInsuranceClaimSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BaseInsuranceClaimSerializer(insurances, many=True, context={"request": request})
            return Response(serializer.data)
