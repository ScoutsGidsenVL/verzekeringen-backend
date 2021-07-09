from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import (
    InsuranceCostOutputSerializer,
    InsuranceListOutputSerializer,
    BaseInsuranceClaimSerializer,
    InsuranceClaimInputSerializer, InsuranceClaimDetailOutputSerializer
)
from ...models.insurance_claim import InsuranceClaim
from ...services import InsuranceClaimService


class InsuranceClaimViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["date"]
    ordering = ["-date"]

    def get_queryset(self):
        return InsuranceClaim.objects.all()

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimDetailOutputSerializer})
    def retrieve(self, request, pk=None):
        claim = self.get_object()
        serializer = InsuranceClaimDetailOutputSerializer(claim)

        return Response(serializer.data)

    @swagger_auto_schema(responses={status.HTTP_200_OK: BaseInsuranceClaimSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        if page is not None:
            serializer = BaseInsuranceClaimSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = BaseInsuranceClaimSerializer(insurances, many=True)
            return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InsuranceClaimInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceClaimDetailOutputSerializer},
    )
    def create(self, request):
        input_serializer = InsuranceClaimInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        claim = InsuranceClaimService.insurance_claim_create(created_by=request.user, **input_serializer.validated_data)

        output_serializer = InsuranceClaimDetailOutputSerializer(claim,  context={"request": request})
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    #
    # # Activity
    # @swagger_auto_schema(
    #     request_body=ActivityInsuranceCreateInputSerializer,
    #     responses={status.HTTP_201_CREATED: ActivityInsuranceDetailOutputSerializer},
    # )
    # @action(methods=["post"], detail=False, url_path="activity")
    # def create_activity(self, request):
    #     input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
    #     input_serializer.is_valid(raise_exception=True)
    #
    #     created_insurance = ActivityInsuranceService.activity_insurance_create(
    #         **input_serializer.validated_data, created_by=request.user
    #     )
    #
    #     output_serializer = ActivityInsuranceDetailOutputSerializer(created_insurance)
    #
    #     return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    #
    # @swagger_auto_schema(
    #     request_body=ActivityInsuranceCreateInputSerializer,
    #     responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    # )
    # @action(methods=["post"], detail=False, url_path="activity/cost")
    # def cost_calculation_activity(self, request):
    #     input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
    #     input_serializer.is_valid(raise_exception=True)
    #
    #     cost = ActivityInsuranceService.activity_insurance_cost_calculation(
    #         **input_serializer.validated_data, created_by=request.user
    #     )
    #
    #     output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})
    #
    #     return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    #
    # @swagger_auto_schema(
    #     request_body=ActivityInsuranceCreateInputSerializer,
    #     responses={status.HTTP_201_CREATED: ActivityInsuranceDetailOutputSerializer},
    # )
    # @action(methods=["put"], detail=False, url_path="activity/(?P<pk>\d+)")
    # def update_activity(self, request, pk=None):
    #     existing_insurance = get_object_or_404(ActivityInsurance.objects.all().editable().allowed(request.user), pk=pk)
    #     input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
    #     input_serializer.is_valid(raise_exception=True)
    #
    #     updated_insurance = ActivityInsuranceService.activity_insurance_update(
    #         insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
    #     )
    #
    #     output_serializer = ActivityInsuranceDetailOutputSerializer(updated_insurance)
    #
    #     return Response(output_serializer.data, status=status.HTTP_201_CREATED)