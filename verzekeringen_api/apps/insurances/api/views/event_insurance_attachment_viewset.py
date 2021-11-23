import logging

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import status, serializers, viewsets, permissions
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_FILE, TYPE_ARRAY

from apps.insurances.models import EventInsurance, EventInsuranceAttachment
from apps.insurances.services import EventInsuranceAttachmentService
from apps.insurances.api.serializers import (
    EventInsuranceAttachmentUploadSerializer,
    EventInsuranceAttachmentSerializer,
)

responses = {
    status.HTTP_400_BAD_REQUEST: Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING)),
    status.HTTP_404_NOT_FOUND: Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}),
}


logger = logging.getLogger(__name__)


class EventInsuranceAttachmentViewSet(viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = EventInsuranceAttachment.objects.all()
    serializer_class = EventInsuranceAttachmentUploadSerializer
    service = EventInsuranceAttachmentService()

    @swagger_auto_schema(
        request_body=EventInsuranceAttachmentUploadSerializer,
        responses={status.HTTP_201_CREATED: EventInsuranceAttachmentSerializer},
        tags=["Files"],
    )
    def create(self, request):
        serializer = EventInsuranceAttachmentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        event_insurance_id = data.get("event_insurance", None)

        logger.debug("Received a file upload request for event insurance %s", event_insurance_id)

        if not event_insurance_id:
            return HttpResponse(404, "Event insurance instance id not supplied with file upload !")

        event_insurance = EventInsurance.objects.get(pk=event_insurance_id)
        if not event_insurance:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Event insurance instance not found !"},
            )

        if not event_insurance.is_accepted():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Event participant list can only be uploaded after the insurance was accepted !"},
            )

        if EventInsuranceAttachment.objects.filter(event_insurance=event_insurance):
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Event insurance already has a participant list !"},
            )

        try:
            result = self.service.store_attachment(uploaded_file=data.get("file"), event_insurance=event_insurance)
        except ValidationError as e:
            raise serializers.ValidationError("; ".join(e.messages))

        output_serializer = EventInsuranceAttachmentSerializer(result, context={"request": request})

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
        # attachement = get_object_or_404(EventInsuranceAttachment.objects, pk=pk)
        # response = HttpResponse(attachement.file, content_type=attachement.content_type)
        # response["Content-Disposition"] = "attachment; filename={}".format(attachement.file.name)
        # return response
        attachment = get_object_or_404(EventInsuranceAttachment.objects, pk=pk)
        output_serializer = EventInsuranceAttachmentSerializer(attachment, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

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
        attachement: EventInsuranceAttachment = get_object_or_404(EventInsuranceAttachment.objects, pk=pk)
        attachement.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
