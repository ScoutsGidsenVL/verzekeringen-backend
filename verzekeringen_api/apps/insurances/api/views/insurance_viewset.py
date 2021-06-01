from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import (
    InsuranceListOutputSerializer,
    ActivityInsuranceDetailOutputSerializer,
    ActivityInsuranceCreateInputSerializer,
    TemporaryInsuranceDetailOutputSerializer,
    TemporaryInsuranceCreateInputSerializer,
)
from ...models import InsuranceType, BaseInsurance, ActivityInsurance, TemporaryInsurance
from ...services import ActivityInsuranceService, TemporaryInsuranceService


class InsuranceViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    def get_queryset(self):
        return BaseInsurance.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceListOutputSerializer})
    def retrieve(self, request, pk=None):
        insurance = self.get_object()

        if insurance.type_id == 1:
            serializer = ActivityInsuranceDetailOutputSerializer(insurance.activity_child)
        elif insurance.type_id == 2:
            serializer = TemporaryInsuranceDetailOutputSerializer(insurance.temporary_child)
        else:
            serializer = InsuranceListOutputSerializer(insurance)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceListOutputSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        if page is not None:
            serializer = InsuranceListOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InsuranceListOutputSerializer(insurances, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=ActivityInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: ActivityInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="activity")
    def create_activity(self, request):
        input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = ActivityInsuranceService.activity_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = ActivityInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ActivityInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: ActivityInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="activity/(?P<pk>\d+)")
    def update_activity(self, request, pk=None):
        existing_insurance = get_object_or_404(ActivityInsurance.objects.all(), pk=pk)
        input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = ActivityInsuranceService.activity_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = ActivityInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="temporary")
    def create_temporary(self, request):
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = TemporaryInsuranceService.temporary_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="temporary/(?P<pk>\d+)")
    def update_temporary(self, request, pk=None):
        existing_insurance = get_object_or_404(TemporaryInsurance.objects.all(), pk=pk)
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TemporaryInsuranceService.temporary_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
