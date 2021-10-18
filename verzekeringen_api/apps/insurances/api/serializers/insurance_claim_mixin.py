from rest_framework import serializers

from apps.insurances.api.serializer_extensions import PermissionRequiredField


class InsuranceClaimAdmistrativeFieldsMixin(metaclass=serializers.SerializerMetaclass):
    note = PermissionRequiredField(
        permission="can_view_note_and_case_number", field=serializers.CharField(max_length=1024), required=False
    )
    case_number = PermissionRequiredField(
        permission="can_view_note_and_case_number", field=serializers.CharField(max_length=30), required=False
    )
