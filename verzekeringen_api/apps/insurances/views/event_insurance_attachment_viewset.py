import datetime
import logging

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import status, serializers, viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_FILE, TYPE_ARRAY
from apps.utils.utils import AuthenticationHelper

from apps.insurances.models import EventInsuranceAttachment
from apps.insurances.services import EventInsuranceAttachmentService
from apps.insurances.serializers import (
    EventInsuranceAttachmentUploadSerializer,
    EventInsuranceAttachmentSerializer,
)

from scouts_insurances.insurances.models import EventInsurance

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
        insurance_id = data.get("insurance", None)

        logger.debug("Received a file upload request for insurance %s", insurance_id)

        if not insurance_id:
            return HttpResponse(404, "Insurance instance id not supplied with file upload !")

        insurance = EventInsurance.objects.get(pk=insurance_id)

        if not insurance:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Insurance instance not found !"},
            )

        AuthenticationHelper.has_rights_for_group(request.user, insurance.scouts_group.group_admin_id)

        if not insurance.accepted:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Participant list can only be uploaded after the insurance was accepted !"},
            )

        file = EventInsuranceAttachment.objects.filter(insurance=insurance)
        if file:
            file.delete()

        try:
            result = self.service.store_attachment(uploaded_file=data.get("file"), insurance=insurance)
        except ValidationError as e:
            raise serializers.ValidationError("; ".join(e.messages))

        output_serializer = EventInsuranceAttachmentSerializer(result, context={"request": request})
        insurance._attachment = datetime.datetime.now()
        insurance.save()
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
        attachment = get_object_or_404(EventInsuranceAttachment.objects, pk=pk)
        output_serializer = EventInsuranceAttachmentSerializer(attachment, context={"request": request})

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
        attachment = get_object_or_404(EventInsuranceAttachment.objects, pk=pk)
        group = attachment.insurance.scouts_group.group_admin_id
        AuthenticationHelper.has_rights_for_group(request.user, group)
        response = HttpResponse(attachment.file.file, content_type=attachment.file.content_type)
        response["Content-Disposition"] = "attachment; filename={}".format(str(attachment.file.file))
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
        attachment: EventInsuranceAttachment = get_object_or_404(EventInsuranceAttachment.objects, pk=pk)
        group = attachment.insurance.scouts_group.group_admin_id
        AuthenticationHelper.has_rights_for_group(request.user, group)
        attachment.delete()
        attachment.insurance._attachment = None
        attachment.insurance.save()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
