import logging
from datetime import datetime

from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.members.services import MemberService
from apps.insurances.models import BaseInsurance, InsuranceType
from apps.insurances.models.enums import InsuranceStatus


logger = logging.getLogger(__name__)


class BaseInsuranceService:
    def base_insurance_creation_fields(
        self,
        *,
        type: InsuranceType,
        group_admin_id: str,
        start_date: datetime,
        end_date: datetime,
        responsible_phone_number: str,
        created_by: settings.AUTH_USER_MODEL,
        comment: str = "",
        id: str = None,
    ) -> dict:
        # validate group
        group_object = next(
            (
                scouts_group
                for scouts_group in created_by.scouts_groups
                if scouts_group.group_admin_id == group_admin_id
            ),
            None,
        )
        if not group_object:
            raise ValidationError("Given group %s is not a valid group of user" % group_admin_id)
        member = MemberService.member_create_from_user(user=created_by, phone_number=responsible_phone_number)
        fields = {
            "status": InsuranceStatus.NEW,
            "type": type,
            "group": group_object,
            "start_date": start_date,
            "end_date": end_date,
            "responsible_member": member,
            "comment": comment,
            "created_on": timezone.now(),
            "id": id,
        }

        return fields

    def base_insurance_delete_relations(self, *, insurance: BaseInsurance):
        insurance.responsible_member.delete()
        return insurance
