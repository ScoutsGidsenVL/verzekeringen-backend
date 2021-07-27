from rest_framework.parsers import MultiPartParser
from rest_framework import views, status, serializers, permissions, viewsets
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from drf_yasg2.utils import swagger_auto_schema
from drf_yasg2.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_FILE, TYPE_ARRAY
from .serializers import UploadFileInputSerializer, UploadFileOutputSerializer
from ..models import InsuranceClaimAttachment
from ..services.file_service import store_attachment

responses = {
    status.HTTP_400_BAD_REQUEST: Schema(
        type=TYPE_ARRAY,
        items=Schema(
            type=TYPE_STRING
        )
    ),
    status.HTTP_404_NOT_FOUND: Schema(
        type=TYPE_OBJECT,
        properties={
            'detail': Schema(type=TYPE_STRING)
        }
    )
}


class FileViewSet(viewsets.GenericViewSet):
    parser_classes = [MultiPartParser]

    @swagger_auto_schema(
        request_body=UploadFileInputSerializer,
        responses={status.HTTP_201_CREATED: UploadFileOutputSerializer},
        tags=['Files'],
    )
    def create(self, request):
        serializer = UploadFileInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        claim = data.get('insurance_claim')

        if not claim:
            return HttpResponse(404, "Insurance claim not found")


        if InsuranceClaimAttachment.objects.filter(insurance_claim=claim):
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"message": "Attachment already have file!"})

        try:
            result = store_attachment(uploaded_file=data.get("file"), claim=claim)
        except ValidationError as e:
            raise serializers.ValidationError("; ".join(e.messages))
        url = request.build_absolute_uri("/api/files/download/" + str(result.id))
        output_serializer = UploadFileOutputSerializer({"url": url, "id": str(result.id)})

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        responses={
            **responses,
            status.HTTP_200_OK: Schema(
                type=TYPE_FILE,
            ),
        },
        tags=['Files'],
    )
    def retrieve(self, request, pk=None):
        attachement = get_object_or_404(InsuranceClaimAttachment.objects, pk=pk)
        return HttpResponse(attachement.file, content_type=attachement.content_type)

    @swagger_auto_schema(
        responses={
            **responses,
            status.HTTP_204_NO_CONTENT: Schema(
                type=TYPE_STRING,
            ),
        },
        tags=['Files'],
    )
    def destroy(self, request, pk):
        attachement: InsuranceClaimAttachment = get_object_or_404(InsuranceClaimAttachment.objects, pk=pk)
        attachement.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
