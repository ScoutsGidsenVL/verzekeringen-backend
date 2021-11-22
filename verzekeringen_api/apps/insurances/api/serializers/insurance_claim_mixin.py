from rest_framework import serializers

from apps.insurances.api.serializer_extensions import PermissionRequiredField


class InsuranceClaimAdmistrativeFieldsMixin(metaclass=serializers.SerializerMetaclass):
    pass
