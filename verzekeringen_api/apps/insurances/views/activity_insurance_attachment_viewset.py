import logging

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import status, serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_FILE, TYPE_ARRAY

from apps.insurances.models import ActivityInsuranceAttachment
from apps.insurances.serializers import (
    ActivityInsuranceAttachmentUploadSerializer,
    ActivityInsuranceAttachmentSerializer,
)
from apps.insurances.services import ActivityInsuranceAttachmentService

from scouts_insurances.insurances.models import ActivityInsurance

responses = {
    status.HTTP_400_BAD_REQUEST: Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING)),
    status.HTTP_404_NOT_FOUND: Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}),
}


logger = logging.getLogger(__name__)


class ActivityInsuranceAttachmentViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ActivityInsuranceAttachment.objects.all()
    serializer_class = ActivityInsuranceAttachmentUploadSerializer
    service = ActivityInsuranceAttachmentService()

    @swagger_auto_schema(
        request_body=ActivityInsuranceAttachmentUploadSerializer,
        responses={status.HTTP_201_CREATED: ActivityInsuranceAttachmentSerializer},
        tags=["Files"],
    )
    def create(self, request):
        serializer = ActivityInsuranceAttachmentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        insurance_id = data.get("insurance", None)

        logger.debug("Received a file upload request for insurance %s", insurance_id)

        if not insurance_id:
            return HttpResponse(404, "Insurance instance id not supplied with file upload !")

        insurance = ActivityInsurance.objects.get(pk=insurance_id)
        if not insurance:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Insurance instance not found !"},
            )

        if not insurance.accepted:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Participant list can only be uploaded after the insurance was accepted !"},
            )

        file = ActivityInsuranceAttachment.objects.filter(insurance=insurance)
        if file:
            file.delete()

        try:
            result = self.service.store_attachment(uploaded_file=data.get("file"), insurance=insurance)
        except ValidationError as e:
            raise serializers.ValidationError("; ".join(e.messages))

        output_serializer = ActivityInsuranceAttachmentSerializer(result, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            **responses,
            status.HTTP_200_OK: Schema(
                type=TYPE_FILE,
            ),
        },
        tags=["Files"],
    )
    def retrieve(self, request, pk=None):
        attachment = get_object_or_404(ActivityInsuranceAttachment.objects, pk=pk)
        output_serializer = ActivityInsuranceAttachmentSerializer(attachment, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={
            **responses,
            status.HTTP_200_OK: Schema(
                type=TYPE_FILE,
            ),
        },
        tags=["Files"],
    )
    @action(methods=["get"], detail=True, url_path="download")
    def download(self, request, pk=None):
        attachment = get_object_or_404(ActivityInsuranceAttachment.objects, pk=pk)
        response = HttpResponse(attachment.file, content_type=attachment.content_type)
        response["Content-Disposition"] = "attachment; filename={}".format(attachment.file.name)
        return response

    @swagger_auto_schema(
        responses={
            **responses,
            status.HTTP_204_NO_CONTENT: Schema(
                type=TYPE_STRING,
            ),
        },
        tags=["Files"],
    )
    def destroy(self, request, pk):
        attachement: ActivityInsuranceAttachment = get_object_or_404(ActivityInsuranceAttachment.objects, pk=pk)
        attachement.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
