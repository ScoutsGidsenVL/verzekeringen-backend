import logging
from datetime import datetime

from django.db import models
from django.db.models import Q
from django.conf import settings

from scouts_insurances.people.models import NonMember
from scouts_insurances.equipment.models import Equipment
from scouts_insurances.insurances.models import (
    NonMemberTemporaryInsurance,
    ParticipantTemporaryVehicleInsurance,
    ParticipantTravelAssistanceInsurance,
)


logger = logging.getLogger(__name__)


class InuitsNonMemberQuerySet(models.QuerySet):

    FIELD_EQUIPMENT = Equipment.owner_non_member.field.name
    # Links a non-member to a temporary insurance through a jointable
    FIELD_NON_MEMBER_TEMPORARY_INSURANCE = NonMemberTemporaryInsurance.non_member_id.field.name
    # Links a non-member to a temporary vehicle insurance through a jointable
    FIELD_TEMPORARY_VEHICLE_INSURANCE = ParticipantTemporaryVehicleInsurance.participant.field.name
    # Links a non-member to a travel assistance insurance through a jointable
    FIELD_TRAVEL_ASSISTANCE = ParticipantTravelAssistanceInsurance.participant.field.name

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def allowed(self, user: settings.AUTH_USER_MODEL):
        groups = [group.group_admin_id for group in user.scouts_groups]
        return self.filter(group_admin_id__in=groups)
    
    def not_currently_temporarily_insured(self, user: settings.AUTH_USER_MODEL, start: datetime, end: datetime, inuits_non_members: list = None):
        from scouts_insurances.insurances.models.enums import InsuranceTypeEnum

        non_members = NonMember.objects.get_queryset().currently_insured(user, start, end, inuits_non_members, InsuranceTypeEnum.TEMPORARY)
        logger.debug(f"non-members: {non_members}")
        
        filtered = []
        non_member_ids = [non_member.inuits_id for non_member in non_members]
        
        for inuits_non_member in inuits_non_members:
            if inuits_non_member.id not in non_member_ids:
                filtered.append(inuits_non_member)

        return filtered

    # def allowed(self, user: settings.AUTH_USER_MODEL):
    #     groups = [group.group_admin_id for group in user.scouts_groups]
    #     return self.filter(
    #         # Equipment (vrzkmateriaal)
    #         Q(template__non_member__equipment__insurance__insurance_parent___group_group_admin_id__in=groups)
    #         # NonMemberTemporaryInsurance (vrzknietledentijd)
    #         | Q(
    #             template__non_member__temporary__temporary_insurance__insurance_parent___group_group_admin_id__in=groups
    #         )
    #         # ParticipantTemporaryVehicleInsurance (vrzktijdautonietleden)
    #         | Q(template__non_member__temporary_vehicle__insurance__insurance_parent___group_group_admin_id__in=groups)
    #         # ParticipantTravelAssistanceInsurance (vrzkassistpassagier)
    #         | Q(template__non_member__travel__temporary_insurance__insurance_parent___group_group_admin_id__in=groups)
    #     )

    # def currently_insured(self, start: datetime, end: datetime):
    #     return self.filter(
    #         # Equipment (vrzkmateriaal)
    #         (
    #             Q(template__non_member__equipment__insurance__insurance_parent__start_date__gte=start)
    #             and Q(template__non_member__equipment__insurance__insurance_parent__end_date__lte=end)
    #         )
    #         # NonMemberTemporaryInsurance (vrzknietledentijd)
    #         | (
    #             Q(template__non_member__temporary__temporary_insurance__insurance_parent__start_date__gte=start)
    #             and Q(template__non_member__temporary__temporary_insurance__insurance_parent__end_date__lte=end)
    #         )
    #         # ParticipantTemporaryVehicleInsurance (vrzktijdautonietleden)
    #         | (
    #             Q(template__non_member__temporary_vehicle__insurance__insurance_parent__start_date__gte=start)
    #             and Q(template__non_member__temporary_vehicle__insurance__insurance_parent__end_date__lte=end)
    #         )
    #         # ParticipantTravelAssistanceInsurance (vrzkassistpassagier)
    #         | (
    #             Q(template__non_member__travel__temporary_insurance__insurance_parent__start_date__gte=start)
    #             and Q(template__non_member__travel__temporary_insurance__insurance_parent__end_date__lte=end)
    #         )
    #     )


class InuitsNonMemberManager(models.Manager):
    def get_queryset(self):
        # Return InuitsNonMember instances that can show up in searches
        return InuitsNonMemberQuerySet(self.model, using=self._db)
