import logging

from django.core.exceptions import ValidationError
from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters, parsers, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_yasg2.utils import swagger_auto_schema

from apps.insurances.serializers import (
    InsuranceClaimAttachmentUploadSerializer,
    InsuranceClaimSerializer,
    InsuranceClaimCreateDataSerializer,
)
from apps.insurances.filters import InsuranceClaimFilter
from apps.insurances.models import InsuranceClaim
from apps.insurances.permissions import InsuranceClaimsPermission
from apps.insurances.services import InsuranceClaimService

from scouts_auth.auth.permissions import CustomDjangoPermission

from scouts_auth.groupadmin.models import AbstractScoutsMember, AbstractScoutsGroup
from scouts_auth.groupadmin.services import GroupAdmin
from scouts_auth.inuits.utils import MultipartJsonParser
from scouts_auth.inuits.files import StorageService
from apps.utils.utils import AuthenticationHelper


logger = logging.getLogger(__name__)


class InsuranceClaimViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend, filters.SearchFilter]
    search_fields = [
        "victim__first_name",
        "victim__last_name",
        "group_group_admin_id",
        "victim__group_admin_id",
        "victim__membership_number"
    ]
    ordering_fields = ["created_on"]
    ordering = ["-date_of_accident", "-created_on"]

    # Filters on the year of the accident
    filterset_class = InsuranceClaimFilter
    service = InsuranceClaimService()
    storage_service = StorageService()
    group_admin_service = GroupAdmin()

    serializer_class = InsuranceClaimSerializer
    parser_classes = [MultipartJsonParser, parsers.JSONParser]
    permission_classes = [InsuranceClaimsPermission]

    def get_queryset(self):
        return InsuranceClaim.objects.all().allowed(self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()

        # appending extra data to context
        if len(self.request.FILES) > 0:
            context.update({"attachments": self.request.FILES})

        return context

    def get_permissions(self):
        current_permissions = super().get_permissions()
        if self.action == "create":
            # current_permissions.append(CustomDjangoPermission("insurances.add_insuranceclaim"))
            # current_permissions.append(CustomDjangoPermission("insurances.change_insuranceclaim"))
            pass
        elif self.action == "list":
            current_permissions.append(CustomDjangoPermission("insurances.list_insuranceclaims"))

        return current_permissions

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimCreateDataSerializer})
    @action(methods=["get"], detail=False, url_path="data")
    def get_create_data(self, request, *args, **kwargs):
        user: settings.AUTH_USER_MODEL = request.user
        # @TODO also for group leader groups
        permitted_scouts_groups = user.get_section_leader_groups()

        data = {"permitted_scouts_groups": permitted_scouts_groups}
        serializer = InsuranceClaimCreateDataSerializer(data, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InsuranceClaimSerializer,
        responses={status.HTTP_201_CREATED: InsuranceClaimSerializer},
    )
    def create(self, request, *args, **kwargs):
        AuthenticationHelper.has_rights_for_group(request.user, request.data["group_group_admin_id"])
        file_serializer_data = {}
        try:
            file_serializer = InsuranceClaimAttachmentUploadSerializer(data=request.FILES)
            file_serializer.is_valid(raise_exception=True)

            file_serializer_data = file_serializer.validated_data
        except Exception as exc:
            logger.error("Error while handling uploaded insurance claim attachment", exc)
            raise ValidationError(
                message={"file": "Error while handling file upload"},
                code=406,
            )
        serializer = InsuranceClaimSerializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        logger.debug("CREATE VALIDATED DATA: %s", validated_data)

        insurance_claim: InsuranceClaim = self.service.create(
            created_by=request.user, file=file_serializer_data, **validated_data
        )


        # There doesn't seem to be a good way to avoid doing this here
        declarant_member: AbstractScoutsMember = self.group_admin_service.get_member_info(
            active_user=request.user, group_admin_id=insurance_claim.declarant.group_admin_id
        )
        insurance_claim.declarant_member = declarant_member
        group: AbstractScoutsGroup = self.group_admin_service.get_group(
            active_user=request.user, group_group_admin_id=insurance_claim.group_group_admin_id
        )
        insurance_claim.group = group

        try:
            self.service.email_claim(insurance_claim)
        except Exception as exc:
            logger.error("Error while sending insurance claim emails", exc)
            raise ValidationError(
                message={"mail": "Error while sending insurance claim emails"},
                code=406,
            )

        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimSerializer})
    def retrieve(self, request, pk=None):
        claim = self.get_object()
        serializer = InsuranceClaimSerializer(claim, context={"request": request})

        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=InsuranceClaimSerializer,
        responses={status.HTTP_200_OK: InsuranceClaimSerializer},
    )
    def partial_update(self, request, pk=None):
        claim = self.get_object()
        AuthenticationHelper.has_rights_for_group(request.user,  claim.group_group_admin_id)
        serializer = InsuranceClaimSerializer(
            data=request.data, instance=InsuranceClaim, context={"request": request}, partial=True
        )
        serializer.is_valid(raise_exception=True)

        updated_claim = InsuranceClaimService.claim_update(claim=claim, **serializer.validated_data)

        output_serializer = InsuranceClaimSerializer(updated_claim, context={"request": request})

        return Response(output_serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(responses={status.HTTP_200_OK: InsuranceClaimSerializer})
    def list(self, request):
        insurances = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(insurances)

        if page is not None:
            serializer = InsuranceClaimSerializer(page, many=True, context={"request": request})
            return self.get_paginated_response(self._filter_claim_list_data(serializer.data))
        else:
            serializer = InsuranceClaimSerializer(insurances, many=True, context={"request": request})
            return Response(self._filter_claim_list_data(serializer.data))

    def _filter_claim_list_data(self, insurance_claims_data):
        fields_to_show = ['id', 'date_of_accident', 'victim', 'group', 'declarant']
        new_claims = []
        for claim in insurance_claims_data:
            new_claim = dict()
            for claim_item in claim:
                if claim_item in fields_to_show:
                    new_claim[claim_item] = claim[claim_item]
            new_claims.append(new_claim)
        return new_claims
