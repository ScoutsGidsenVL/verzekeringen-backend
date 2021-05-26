from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import (
    InsuranceListOutputSerializer,
    ActivityInsuranceDetailOutputSerializer,
    BaseInsuranceCreateInputSerializer,
    ActivityInsuranceCreateInputSerializer,
)
from ...models import InsuranceType, BaseInsurance
from ...services import ActivityInsuranceService


class InsuranceViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["id"]
    ordering = ["id"]

    def get_queryset(self):
        return BaseInsurance.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceListOutputSerializer})
    def retrieve(self, request, pk=None):
        insurance = self.get_object()

        if insurance.type_id == 1:
            serializer = ActivityInsuranceDetailOutputSerializer(insurance.activity_child)
        else:
            serializer = InsuranceListOutputSerializer(insurance)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceListOutputSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        if page is not None:
            print(page)
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
