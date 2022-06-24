from datetime import datetime
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Q


class NonMemberQuerySet(models.QuerySet):
    def template_editable(self, user: settings.AUTH_USER_MODEL):
        return self.filter(Q(template__editable=True))

    def editable(self, user: settings.AUTH_USER_MODEL):
        from scouts_insurances.insurances.models.enums import InsuranceStatus

        return self.filter(
            # TemporaryInsurance
            # MANY_TO_MANY: NonMemberTemporaryInsurance (insurance field: temporary_insurance, related_name: temporary)
            Q(
                temporary__temporary_insurance___status__in=[
                    InsuranceStatus.NEW,
                    InsuranceStatus.WAITING,
                ]
            )
            |
            # TemporaryVehicleInsurance
            # MANY-TO-MANY: ParticipantTemporaryVehicleInsurance (insurance field: insurance, related_name: temporary_vehicle)
            Q(
                temporary_vehicle__insurance___status__in=[
                    InsuranceStatus.NEW,
                    InsuranceStatus.WAITING,
                ]
            )
            |
            # TravelAssistanceInsurance
            # MANY-TO-MANY: ParticipantTravelAssistanceInsurance (insurance field: temporary_insurance, related_name: travel)
            Q(
                travel__temporary_insurance___status__in=[
                    InsuranceStatus.NEW,
                    InsuranceStatus.WAITING,
                ]
            )
        )

    def non_editable(self, user: settings.AUTH_USER_MODEL):
        from scouts_insurances.insurances.models.enums import InsuranceStatus

        return self.filter(
            # TemporaryInsurance
            # MANY_TO_MANY: NonMemberTemporaryInsurance (insurance field: temporary_insurance, related_name: temporary)
            Q(
                temporary__temporary_insurance___status__in=[
                    InsuranceStatus.ACCEPTED,
                    InsuranceStatus.BILLED,
                    InsuranceStatus.REJECTED,
                ]
            )
            |
            # TemporaryVehicleInsurance
            # MANY-TO-MANY: ParticipantTemporaryVehicleInsurance (insurance field: insurance, related_name: temporary_vehicle)
            Q(
                temporary_vehicle__insurance___status__in=[
                    InsuranceStatus.ACCEPTED,
                    InsuranceStatus.BILLED,
                    InsuranceStatus.REJECTED,
                ]
            )
            |
            # TravelAssistanceInsurance
            # MANY-TO-MANY: ParticipantTravelAssistanceInsurance (insurance field: temporary_insurance, related_name: travel)
            Q(
                travel__temporary_insurance___status__in=[
                    InsuranceStatus.ACCEPTED,
                    InsuranceStatus.BILLED,
                    InsuranceStatus.REJECTED,
                ]
            )
        )
        # equipment insurance ?

    def currently_insured(self, start: datetime, end: datetime, inuits_non_member_ids: list = None, type=None):
        from scouts_insurances.insurances.models.enums import InsuranceTypeEnum

        if inuits_non_member_ids and type:
            if type is InsuranceTypeEnum.TEMPORARY:
                return self.filter(Q(inuits_id__in=inuits_non_member_ids))
            else:
                return self.filter(
                    Q(temporary_insurances__non_members__in=inuits_non_member_ids)
                    and Q(insurance_parent__start_date__gte=start)
                    and Q(insurance_parent__end_date__lte=end)
                )


class NonMemberManager(models.Manager):
    def get_queryset(self):
        return NonMemberQuerySet(self.model, using=self._db)
