from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.api.serializers import (
    InsuranceCostOutputSerializer,
    InsuranceListOutputSerializer,
    ActivityInsuranceDetailOutputSerializer,
    ActivityInsuranceCreateInputSerializer,
    TemporaryInsuranceDetailOutputSerializer,
    TemporaryInsuranceCreateInputSerializer,
    TravelAssistanceInsuranceDetailOutputSerializer,
    TravelAssistanceInsuranceCreateInputSerializer,
    TemporaryVehicleInsuranceDetailOutputSerializer,
    TemporaryVehicleInsuranceCreateInputSerializer,
    EventInsuranceDetailOutputSerializer,
    EventInsuranceCreateInputSerializer,
    EquipmentInsuranceDetailOutputSerializer,
    EquipmentInsuranceCreateInputSerializer,
)
from apps.insurances.models import (
    BaseInsurance,
    ActivityInsurance,
    TemporaryInsurance,
    TravelAssistanceInsurance,
    TemporaryVehicleInsurance,
    EventInsurance,
    EquipmentInsurance,
)
from apps.insurances.services import (
    ActivityInsuranceService,
    TemporaryInsuranceService,
    TravelAssistanceInsuranceService,
    TemporaryVehicleInsuranceService,
    EventInsuranceService,
    EquipmentInsuranceService,
)


class InsuranceViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ["_group_group_admin_id"]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    activity_insurance_service = ActivityInsuranceService()
    temporary_insurance_service = TemporaryInsuranceService()
    travel_assistance_insurance_service = TravelAssistanceInsuranceService()
    temporary_vehicle_insurance_service = TemporaryVehicleInsuranceService()
    event_insurance_service = EventInsuranceService()
    equipment_insurance_service = EquipmentInsuranceService()

    def get_queryset(self):
        return BaseInsurance.objects.all().allowed(self.request.user)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceListOutputSerializer})
    def retrieve(self, request, pk=None):
        insurance: BaseInsurance = get_object_or_404(self.get_queryset(), pk=pk)

        if insurance.type.id == 1:
            serializer = ActivityInsuranceDetailOutputSerializer(insurance.activity_child)
        elif insurance.type.id == 2:
            serializer = TemporaryInsuranceDetailOutputSerializer(insurance.temporary_child)
        elif insurance.type.id in (3, 4):
            serializer = TravelAssistanceInsuranceDetailOutputSerializer(insurance.travel_assistance_child)
        elif insurance.type.id == 5:
            serializer = TemporaryVehicleInsuranceDetailOutputSerializer(insurance.temporary_vehicle_child)
        elif insurance.type.id == 6:
            serializer = EquipmentInsuranceDetailOutputSerializer(insurance.equipment_child)
        elif insurance.type.id == 10:
            serializer = EventInsuranceDetailOutputSerializer(insurance.event_child, context={"request": request})
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

    # Activity
    @swagger_auto_schema(
        request_body=ActivityInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: ActivityInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="activity")
    def create_activity(self, request):
        input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = self.activity_insurance_service.activity_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = ActivityInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ActivityInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="activity/cost")
    def cost_calculation_activity(self, request):
        input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.activity_insurance_service.activity_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=ActivityInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: ActivityInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="activity/(?P<pk>\d+)")
    def update_activity(self, request, pk=None):
        existing_insurance = get_object_or_404(
            ActivityInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.activity_insurance_service.activity_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = ActivityInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # Temporary
    @swagger_auto_schema(
        request_body=TemporaryInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="temporary")
    def create_temporary(self, request):
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = self.temporary_insurance_service.temporary_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="temporary/cost")
    def cost_calculation_temporary(self, request):
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.temporary_insurance_service.temporary_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="temporary/(?P<pk>\d+)")
    def update_temporary(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TemporaryInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.temporary_insurance_service.temporary_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # Travel assistance
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

        created_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TravelAssistanceInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="travel_assistance/cost")
    def cost_calculation_travel_assistance(self, request):
        input_serializer = TravelAssistanceInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        cost = self.travel_assistance_insurance_service.travel_assistance_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TravelAssistanceInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TravelAssistanceInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="travel_assistance/(?P<pk>\d+)")
    def update_travel_assistance(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TravelAssistanceInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = TravelAssistanceInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.travel_assistance_insurance_service.travel_assistance_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TravelAssistanceInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # Temporary vehicle
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

        created_insurance = self.temporary_vehicle_insurance_service.temporary_vehicle_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryVehicleInsuranceDetailOutputSerializer(
            created_insurance, context=created_insurance
        )

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryVehicleInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="temporary_vehicle/cost")
    def cost_calculation_temporary_vehicle(self, request):
        input_serializer = TemporaryVehicleInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        cost = self.temporary_vehicle_insurance_service.temporary_vehicle_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=TemporaryVehicleInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: TemporaryVehicleInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="temporary_vehicle/(?P<pk>\d+)")
    def update_temporary_vehicle(self, request, pk=None):
        existing_insurance = get_object_or_404(
            TemporaryVehicleInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = TemporaryVehicleInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.temporary_vehicle_insurance_service.temporary_vehicle_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryVehicleInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # Event
    @swagger_auto_schema(
        request_body=EventInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: EventInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="event")
    def create_event(self, request):
        input_serializer = EventInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = self.event_insurance_service.event_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EventInsuranceDetailOutputSerializer(created_insurance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="event/cost")
    def cost_calculation_event(self, request):
        input_serializer = EventInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.event_insurance_service.event_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: EventInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="event/(?P<pk>\d+)")
    def update_event(self, request, pk=None):
        existing_insurance = get_object_or_404(
            EventInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = EventInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.event_insurance_service.event_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EventInsuranceDetailOutputSerializer(updated_insurance, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    # Equipment
    @swagger_auto_schema(
        request_body=EquipmentInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: EquipmentInsuranceDetailOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="equipment")
    def create_equipment(self, request):
        input_serializer = EquipmentInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        created_insurance = self.equipment_insurance_service.equipment_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EquipmentInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EquipmentInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="equipment/cost")
    def cost_calculation_equipment(self, request):
        input_serializer = EquipmentInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = self.equipment_insurance_service.equipment_insurance_cost_calculation(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceCostOutputSerializer({"total_cost": cost})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EquipmentInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: EquipmentInsuranceDetailOutputSerializer},
    )
    @action(methods=["put"], detail=False, url_path="equipment/(?P<pk>\d+)")
    def update_equipment(self, request, pk=None):
        existing_insurance = get_object_or_404(
            EquipmentInsurance.objects.all().editable(request.user).allowed(request.user), pk=pk
        )
        input_serializer = EquipmentInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = self.equipment_insurance_service.equipment_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EquipmentInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
