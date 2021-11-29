import logging
from datetime import datetime
from decimal import Decimal

from django.db import transaction
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

from scouts_insurances.people.models import Member
from scouts_insurances.people.services import MemberService
from scouts_insurances.insurances.models import BaseInsurance, InsuranceType
from scouts_insurances.insurances.models.enums import InsuranceStatus

from scouts_auth.groupadmin.models import ScoutsGroup

# from scouts_insurances.insurances.services import InsuranceMailService


logger = logging.getLogger(__name__)


class BaseInsuranceService:
    # mail_service = InsuranceMailService()
    member_service = MemberService()

    def base_insurance_creation_fields(
        self,
        *,
        id: str = "",
        status: str = "",
        scouts_group: ScoutsGroup = None,
        total_cost: Decimal = None,
        comment: str = "",
        vvksm_comment: str = "",
        created_on: datetime = None,
        responsible_member: Member = None,
        type: InsuranceType,
        start_date: datetime,
        end_date: datetime,
        created_by: settings.AUTH_USER_MODEL,
    ) -> dict:
        # validate group
        group_object = next(
            (
                scouts_group
                for scouts_group in created_by.scouts_groups
                if scouts_group.group_admin_id == scouts_group.group_admin_id
            ),
            None,
        )
        if not group_object:
            raise ValidationError("Given group %s is not a valid group of user" % scouts_group.group_admin_id)
        member = self.member_service.member_create_from_user(user=created_by)
        fields = {
            "status": InsuranceStatus.NEW,
            "type": type,
            "scouts_group": group_object,
            "start_date": start_date,
            "end_date": end_date,
            "responsible_member": member,
            "comment": comment,
            "created_on": timezone.now(),
            "id": id,
        }

        return fields

    @transaction.atomic
    def base_insurance_delete_relations(self, *, insurance: BaseInsurance):
        insurance.responsible_member.delete()
        return insurance

    def handle_insurance_created(self, insurance: BaseInsurance):
        # return self.mail_service.send_insurance(insurance)
        pass
