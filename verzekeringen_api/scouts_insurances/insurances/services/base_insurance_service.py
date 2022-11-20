import logging
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError, PermissionDenied
from scouts_auth.auth.models import User
from scouts_insurances.people.models import Member
from scouts_insurances.people.services import MemberService
from scouts_insurances.insurances.models import BaseInsurance, InsuranceType
from scouts_insurances.insurances.models.enums import InsuranceStatus
from scouts_insurances.insurances.services import InsuranceMailService


from scouts_auth.groupadmin.models import AbstractScoutsGroup

logger = logging.getLogger(__name__)


class BaseInsuranceService:
    mail_service = InsuranceMailService()
    member_service = MemberService()

    def base_insurance_creation_fields(
            self,
            *,
            id: str = None,
            status: str = "",  # Calculated value
            scouts_group: AbstractScoutsGroup = None,
            total_cost: Decimal = None,  # Handled by the BaseInsuranceSerializer
            comment: str = "",
            vvksm_comment: str = "",
            created_on: datetime = None,  # Calculated value
            responsible_member: Member = None,  # Calculated value
            type: InsuranceType = None,
            start_date: datetime = None,
            end_date: datetime = None,
            created_by: settings.AUTH_USER_MODEL,
    ) -> dict:
        # validate group
        group_object = next(
            (group for group in created_by.scouts_groups if group.group_admin_id == scouts_group.group_admin_id),
            None,
        )
        if not group_object:
            raise PermissionDenied(
                {
                    "message": "Given group {} is not a valid group of user".format(
                        scouts_group.group_admin_id
                    )
                }
            )
        member = self.member_service.member_create_from_user(user=created_by)
        fields = {
            "status": InsuranceStatus.NEW,
            "type": type,
            "scouts_group": scouts_group,
            # "start_date": datetime.combine(start_date.date(), datetime.min.time()),
            # "end_date": datetime.combine(end_date.date(), datetime.min.time()),
            "start_date": start_date,
            "end_date": end_date,
            "responsible_member": member,
            "comment": comment,
            "vvksm_comment": vvksm_comment,
            "created_on": datetime.now(),
            "id": id,
        }

        return fields

    @transaction.atomic
    def base_insurance_delete_relations(self, *, insurance: BaseInsurance):
        # insurance.responsible_member.delete() # why?
        return insurance

    def handle_insurance_created(self, insurance: BaseInsurance, created_by: User):
        return self.mail_service.send_insurance(insurance,created_by=created_by)
