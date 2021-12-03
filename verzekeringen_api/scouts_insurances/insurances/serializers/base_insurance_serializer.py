import logging
from decimal import Decimal

from django.core.exceptions import ValidationError
from rest_framework import serializers
from drf_yasg2.utils import swagger_serializer_method

from scouts_insurances.people.serializers import MemberSerializer
from scouts_insurances.insurances.models import BaseInsurance
from scouts_insurances.insurances.serializers import (
    InsuranceTypeSerializer,
    InsuranceCostSerializer,
)

from scouts_auth.groupadmin.models import ScoutsGroup
from scouts_auth.groupadmin.serializers import ScoutsGroupSerializer
from scouts_auth.inuits.serializers import DatetypeAndTimezoneAwareDateTimeSerializerField


logger = logging.getLogger(__name__)


class BaseInsuranceSerializer(serializers.ModelSerializer):
    # id                    pk
    # status                number          optional
    # scouts_group          ScoutsGroup
    # total_cost            decimal         optional
    # comment               max_length=500  optional
    # vvksm_comment         max_length=500  optional
    # created_on            datetime        optional
    # start_date            datetime        optional
    # end_date              datetime        optional
    # responsible_member    Member          required
    # type                  InsuranceType   optional

    status = serializers.SerializerMethodField()
    scouts_group = ScoutsGroupSerializer(required=False)
    # For input
    group_admin_id = serializers.CharField(required=False)
    total_cost = serializers.SerializerMethodField()
    created_on = DatetypeAndTimezoneAwareDateTimeSerializerField(required=False)
    start_date = DatetypeAndTimezoneAwareDateTimeSerializerField()
    end_date = DatetypeAndTimezoneAwareDateTimeSerializerField()
    responsible_member = MemberSerializer(required=False)
    type = InsuranceTypeSerializer(required=False)

    class Meta:
        model = BaseInsurance
        # fields = "__all__"
        exclude = [
            "_status",
            "invoice_number",
            "invoice_date",
            "_group_group_admin_id",
            "_group_location",
            "_group_name",
            "_printed",
            "_finished",
            "_listed",
            "_start_date",
            "_end_date",
            "payment_date",
        ]

    @swagger_serializer_method(serializer_or_field=status)
    def get_status(self, obj: BaseInsurance) -> dict:
        return {"id": obj.status.value, "value": obj.status.value, "label": obj.status.label}

    @swagger_serializer_method(serializer_or_field=ScoutsGroupSerializer)
    def get_scouts_group(self, obj) -> ScoutsGroup:
        return ScoutsGroupSerializer(obj).data

    @swagger_serializer_method(serializer_or_field=InsuranceCostSerializer)
    def get_total_cost(self, obj: BaseInsurance) -> Decimal:
        return InsuranceCostSerializer(obj.total_cost).data

    def validate(self, data: dict) -> dict:
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)

        if start_date is None:
            raise ValidationError("An insurance needs a start date")
        if end_date is None:
            raise ValidationError("An insurance needs an end date")

        scouts_group = data.get("scouts_group", None)
        group_admin_id = data.get("group_admin_id", None)
        if not scouts_group and not group_admin_id:
            raise ValidationError(
                "An insurance needs either a ScoutsGroup instance or the group_admin_id of a scouts group, both are None."
            )

        return super().validate(data)
