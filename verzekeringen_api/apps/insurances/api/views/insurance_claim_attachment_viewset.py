import logging

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from rest_framework import status, serializers, viewsets
from rest_framework.response import Response
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_FILE, TYPE_ARRAY

from apps.insurances.models import InsuranceClaimAttachment
from apps.insurances.services import InsuranceClaimAttachmentService
from apps.insurances.api.serializers import (
    InsuranceClaimAttachmentUploadSerializer,
    InsuranceClaimAttachmentSerializer,
)

responses = {
    status.HTTP_400_BAD_REQUEST: Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_STRING)),
    status.HTTP_404_NOT_FOUND: Schema(type=TYPE_OBJECT, properties={"detail": Schema(type=TYPE_STRING)}),
}


logger = logging.getLogger(__name__)


class InsuranceClaimAttachmentViewSet(viewsets.GenericViewSet):

    queryset = InsuranceClaimAttachment.objects.all()
    serializer_class = InsuranceClaimAttachmentUploadSerializer
    service = InsuranceClaimAttachmentService()

    @swagger_auto_schema(
        request_body=InsuranceClaimAttachmentUploadSerializer,
        responses={status.HTTP_201_CREATED: InsuranceClaimAttachmentSerializer},
        tags=["Files"],
    )
    def create(self, request):
        serializer = InsuranceClaimAttachmentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        claim = data.get("insurance_claim")

        logger.debug("Received a file upload request for claim %s", claim)

        if not claim:
            return HttpResponse(404, "Insurance claim not found")

        if InsuranceClaimAttachment.objects.filter(insurance_claim=claim):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Attachment already have file!"})

        try:
            result = self.service.store_attachment(uploaded_file=data.get("file"), claim=claim)
        except ValidationError as e:
            raise serializers.ValidationError("; ".join(e.messages))

        url = request.build_absolute_uri("/api/files/download/" + str(result.id))
        output_serializer = InsuranceClaimAttachmentSerializer({"url": url, "id": str(result.id)})

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
        attachement = get_object_or_404(InsuranceClaimAttachment.objects, pk=pk)
        response = HttpResponse(attachement.file, content_type=attachement.content_type)
        response["Content-Disposition"] = "attachment; filename={}".format(attachement.file.name)
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
        attachement: InsuranceClaimAttachment = get_object_or_404(InsuranceClaimAttachment.objects, pk=pk)
        attachement.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
