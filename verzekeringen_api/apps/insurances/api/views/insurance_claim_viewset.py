import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, parsers
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.api.serializers import (
    BaseInsuranceClaimSerializer,
    InsuranceClaimInputSerializer,
    InsuranceClaimDetailOutputSerializer,
)
from apps.insurances.api.filters import InsuranceClaimFilter
from apps.insurances.models import InsuranceClaim
from apps.insurances.services import InsuranceClaimService
from inuits.utils import MultipartJsonParser


logger = logging.getLogger(__name__)


class InsuranceClaimViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    search_fields = ["victim__first_name", "victim__last_name", "group_number", "victim__group_admin_id"]
    ordering_fields = ["date"]
    ordering = ["-date"]
    parser_classes = (MultipartJsonParser, parsers.JSONParser)
    # Filters on the year of the accident
    filterset_class = InsuranceClaimFilter
    service = InsuranceClaimService()

    def get_queryset(self):
        return InsuranceClaim.objects.all()

    @swagger_auto_schema(
        request_body=InsuranceClaimInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceClaimDetailOutputSerializer},
    )
    @parser_classes([MultipartJsonParser])
    def create(self, request):
        input_serializer = InsuranceClaimInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)
        data = input_serializer.validated_data
        logger.info("DICT: %s", data)
        claim: InsuranceClaim = self.service.create(created_by=request.user, **data)
        self.service.email_claim(claim=claim)
        output_serializer = InsuranceClaimDetailOutputSerializer(claim, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        claim = self.get_object()
        serializer = InsuranceClaimDetailOutputSerializer(claim, context={"request": request})

        return Response(serializer.data)

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
