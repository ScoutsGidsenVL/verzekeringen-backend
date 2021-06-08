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
    TravelAssistanceInsuranceDetailOutputSerializer,
    TravelAssistanceInsuranceCreateInputSerializer,
    TemporaryVehicleInsuranceDetailOutputSerializer,
    TemporaryVehicleInsuranceCreateInputSerializer,
)
from ...models import (
    InsuranceType,
    BaseInsurance,
    ActivityInsurance,
    TemporaryInsurance,
    TravelAssistanceInsurance,
    TemporaryVehicleInsurance,
)
from ...services import (
    ActivityInsuranceService,
    TemporaryInsuranceService,
    TravelAssistanceInsuranceService,
    TemporaryVehicleInsuranceService,
)


class InsuranceViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    def get_queryset(self):
        return BaseInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceListOutputSerializer})
    def retrieve(self, request, pk=None):
        insurance = self.get_object()

        if insurance.type_id == 1:
            serializer = ActivityInsuranceDetailOutputSerializer(insurance.activity_child)
        elif insurance.type_id == 2:
            serializer = TemporaryInsuranceDetailOutputSerializer(insurance.temporary_child)
        elif insurance.type_id in (3, 4):
            serializer = TravelAssistanceInsuranceDetailOutputSerializer(insurance.travel_assistance_child)
        elif insurance.type_id == 5:
            serializer = TemporaryVehicleInsuranceDetailOutputSerializer(insurance.temporary_vehicle_child)
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
        existing_insurance = get_object_or_404(ActivityInsurance.objects.all().allowed(request.user), pk=pk)
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
        existing_insurance = get_object_or_404(TemporaryInsurance.objects.all().allowed(request.user), pk=pk)
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TemporaryInsuranceService.temporary_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TravelAssistanceInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="travel_assistance")
    def create_travel_assistance(self, request):
        input_serializer = TravelAssistanceInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        created_insurance = TravelAssistanceInsuranceService.travel_assistance_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TravelAssistanceInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TravelAssistanceInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="travel_assistance/(?P<pk>\d+)")
    def update_travel_assistance(self, request, pk=None):
        existing_insurance = get_object_or_404(TravelAssistanceInsurance.objects.all().allowed(request.user), pk=pk)
        input_serializer = TravelAssistanceInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TravelAssistanceInsuranceService.travel_assistance_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TravelAssistanceInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryVehicleInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryVehicleInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="temporary_vehicle")
    def create_temporary_vehicle(self, request):
        input_serializer = TemporaryVehicleInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        created_insurance = TemporaryVehicleInsuranceService.temporary_vehicle_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryVehicleInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryVehicleInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryVehicleInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="temporary_vehicle/(?P<pk>\d+)")
    def update_temporary_vehicle(self, request, pk=None):
        existing_insurance = get_object_or_404(TemporaryVehicleInsurance.objects.all().allowed(request.user), pk=pk)
        input_serializer = TemporaryVehicleInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TemporaryVehicleInsuranceService.temporary_vehicle_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryVehicleInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
