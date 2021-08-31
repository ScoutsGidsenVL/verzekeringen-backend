from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import (
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
from ...models import (
    InsuranceType,
    BaseInsurance,
    ActivityInsurance,
    TemporaryInsurance,
    TravelAssistanceInsurance,
    TemporaryVehicleInsurance,
    EventInsurance,
    EquipmentInsurance,
)
from ...services import (
    ActivityInsuranceService,
    TemporaryInsuranceService,
    TravelAssistanceInsuranceService,
    TemporaryVehicleInsuranceService,
    EventInsuranceService,
    EquipmentInsuranceService,
)


class InsuranceViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['_group_number']
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]

    def get_queryset(self):
        return BaseInsurance.objects\
            .filter(
                created_on__gte=datetime.now() - timedelta(days=3 * 365)
            )\
            .allowed(self.request.user)

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
        elif insurance.type_id == 6:
            serializer = EquipmentInsuranceDetailOutputSerializer(insurance.equipment_child)
        elif insurance.type_id == 10:
            serializer = EventInsuranceDetailOutputSerializer(insurance.event_child)
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

        created_insurance = ActivityInsuranceService.activity_insurance_create(
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

        cost = ActivityInsuranceService.activity_insurance_cost_calculation(
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
        existing_insurance = get_object_or_404(ActivityInsurance.objects.all().editable().allowed(request.user), pk=pk)
        input_serializer = ActivityInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = ActivityInsuranceService.activity_insurance_update(
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

        created_insurance = TemporaryInsuranceService.temporary_insurance_create(
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

        cost = TemporaryInsuranceService.temporary_insurance_cost_calculation(
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
            TemporaryInsurance.objects.all().editable().allowed(request.user), pk=pk
        )
        input_serializer = TemporaryInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TemporaryInsuranceService.temporary_insurance_update(
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

        created_insurance = TravelAssistanceInsuranceService.travel_assistance_insurance_create(
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

        cost = TravelAssistanceInsuranceService.travel_assistance_insurance_cost_calculation(
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
            TravelAssistanceInsurance.objects.all().editable().allowed(request.user), pk=pk
        )
        input_serializer = TravelAssistanceInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TravelAssistanceInsuranceService.travel_assistance_insurance_update(
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

        created_insurance = TemporaryVehicleInsuranceService.temporary_vehicle_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = TemporaryVehicleInsuranceDetailOutputSerializer(created_insurance, context=created_insurance)

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

        cost = TemporaryVehicleInsuranceService.temporary_vehicle_insurance_cost_calculation(
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
            TemporaryVehicleInsurance.objects.all().editable().allowed(request.user), pk=pk
        )
        input_serializer = TemporaryVehicleInsuranceCreateInputSerializer(
            data=request.data, context={"request": request}
        )
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = TemporaryVehicleInsuranceService.temporary_vehicle_insurance_update(
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

        created_insurance = EventInsuranceService.event_insurance_create(
            **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EventInsuranceDetailOutputSerializer(created_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        request_body=EventInsuranceCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceCostOutputSerializer},
    )
    @action(methods=["post"], detail=False, url_path="event/cost")
    def cost_calculation_event(self, request):
        input_serializer = EventInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        cost = EventInsuranceService.event_insurance_cost_calculation(
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
        existing_insurance = get_object_or_404(EventInsurance.objects.all().editable().allowed(request.user), pk=pk)
        input_serializer = EventInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = EventInsuranceService.event_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EventInsuranceDetailOutputSerializer(updated_insurance)

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

        created_insurance = EquipmentInsuranceService.equipment_insurance_create(
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

        cost = EquipmentInsuranceService.equipment_insurance_cost_calculation(
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
            EquipmentInsurance.objects.all().editable().allowed(request.user), pk=pk
        )
        input_serializer = EquipmentInsuranceCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)

        updated_insurance = EquipmentInsuranceService.equipment_insurance_update(
            insurance=existing_insurance, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = EquipmentInsuranceDetailOutputSerializer(updated_insurance)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
