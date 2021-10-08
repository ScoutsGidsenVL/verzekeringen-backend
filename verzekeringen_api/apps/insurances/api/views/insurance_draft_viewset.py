from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from ..serializers import InsuranceDraftOutputSerializer, InsuranceDraftCreateInputSerializer
from ...models import InsuranceDraft
from ...services import InsuranceDraftService


class InsuranceDraftViewSet(viewsets.GenericViewSet):
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_on"]
    ordering = ["-created_on"]
    service = InsuranceDraftService()

    def get_queryset(self):
        return InsuranceDraft.objects.all().allowed(self.request.user)

    @swagger_auto_schema(
        request_body=InsuranceDraftCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceDraftOutputSerializer},
    )
    def create(self, request):
        input_serializer = InsuranceDraftCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)
        draft = self.service.insurance_draft_create(**input_serializer.validated_data, created_by=request.user)

        output_serializer = InsuranceDraftOutputSerializer(draft)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceDraftOutputSerializer})
    def retrieve(self, request, pk=None):
        draft = self.get_object()
        serializer = InsuranceDraftOutputSerializer(draft)

    @swagger_auto_schema(
        request_body=InsuranceDraftCreateInputSerializer,
        responses={status.HTTP_201_CREATED: InsuranceDraftOutputSerializer},
    )
    def update(self, request, pk=None):
        draft = self.get_object()
        input_serializer = InsuranceDraftCreateInputSerializer(data=request.data, context={"request": request})
        input_serializer.is_valid(raise_exception=True)
        new_draft = self.service.insurance_draft_update(
            draft=draft, **input_serializer.validated_data, created_by=request.user
        )

        output_serializer = InsuranceDraftOutputSerializer(new_draft)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        draft = self.get_object()
        self.service.insurance_draft_delete(draft=draft)
        return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceDraftOutputSerializer})
    def list(self, request):
        drafts = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(drafts)

        if page is not None:
            serializer = InsuranceDraftOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = InsuranceDraftOutputSerializer(drafts, many=True)
            return Response(serializer.data)
